"""
conftest.py — Fixtures compartidos para todos los tests de SmartStock.

Revisado contra el código real del repo (Proyecto-Backend-main.zip).
Usa una BD de Postgres separada (ej. smartstock_test_db) — el modelo Producto
tiene CheckConstraint a nivel de BD además de validación Pydantic, y SQLite
no los valida igual.
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db

# --- Configuración de BD de pruebas ---
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/smartstock_test_db",
)

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Crea todas las tablas al inicio de la sesión de tests y las elimina al final."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def limpiar_bd():
    """
    Vacía todas las tablas ANTES de cada test individual.

    Sin esto, cada test que crea una categoría/rol/usuario con un nombre
    fijo ("Categoria Test", "admin_test", etc.) choca con el registro que
    dejó el test anterior, porque el TestClient hace commits reales contra
    smartstock_test_db -- no hay rollback automático entre tests.
    """
    with engine.begin() as conn:
        for tabla in reversed(Base.metadata.sorted_tables):
            conn.execute(tabla.delete())
    yield


@pytest.fixture()
def db_session():
    """Sesión de BD limpia para cada test (rollback al final)."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def admin_headers(client):
    """
    Crea un rol y un usuario, hace login, y devuelve headers listos
    para usar en requests protegidos (POST /ventas/ y POST /compras/,
    que son los ÚNICOS endpoints que exigen JWT en este proyecto —
    ver nota de seguridad más abajo).
    """
    rol_response = client.post(
        "/api/v1/roles/", json={"nombre": "admin_test", "descripcion": "rol de pruebas"}
    )
    assert rol_response.status_code == 201, f"No se pudo crear rol: {rol_response.text}"
    rol_id = rol_response.json()["rol_id"]

    usuario_response = client.post(
        "/api/v1/usuarios/",
        json={
            "nombre": "Test Admin",
            "correo": "test_admin@smartstock.com",
            "contrasena": "TestPass123!",
            "rol_id": rol_id,
        },
    )
    assert usuario_response.status_code == 201, f"No se pudo crear usuario: {usuario_response.text}"

    login_response = client.post(
        "/api/v1/auth/login",
        json={"correo": "test_admin@smartstock.com", "contrasena": "TestPass123!"},
    )
    assert login_response.status_code == 200, f"Login falló: {login_response.text}"
    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def categoria_id(client):
    """
    Crea una categoría de prueba y devuelve su categoria_id.
    Nota: este endpoint NO exige autenticación (ver hallazgo de seguridad),
    así que no se necesitan headers aquí.
    """
    response = client.post(
        "/api/v1/categorias/",
        json={"nombre": "Categoria Test", "descripcion": "para pruebas"},
    )
    assert response.status_code == 201, f"No se pudo crear categoría: {response.text}"
    return response.json()["categoria_id"]


@pytest.fixture()
def producto_id(client, categoria_id):
    """Crea un producto de prueba y devuelve su producto_id."""
    response = client.post(
        "/api/v1/productos/",
        json={
            "nombre": "Producto Test",
            "descripcion": "producto para pruebas automatizadas",
            "categoria_id": categoria_id,
            "precio_compra": 5.0,
            "precio_venta": 10.0,
            "unidad_medida": "unidad",
        },
    )
    assert response.status_code == 201, f"No se pudo crear producto: {response.text}"
    return response.json()["producto_id"]


@pytest.fixture()
def producto_con_inventario(client, producto_id):
    """
    Crea el registro de inventario para el producto (stock_actual=0).

    IMPORTANTE: a diferencia de lo que asumimos antes, el inventario NO se
    crea automáticamente al crear un producto -- hay que llamar
    POST /api/v1/inventario/ explícitamente. Si se intenta comprar/vender
    un producto sin este registro previo, el backend responde 500
    (ajustar_stock asume que el registro ya existe). Ver hallazgo en el
    informe de Fase 3/4.
    """
    response = client.post(
        "/api/v1/inventario/",
        json={"producto_id": producto_id, "stock_actual": 0, "stock_minimo": 5},
    )
    assert response.status_code == 201, f"No se pudo crear inventario: {response.text}"
    return producto_id