"""
Tests del módulo de productos.

Revisado contra producto_controller.py / producto_service.py reales:
- La actualización usa PATCH, no PUT.
- El servicio valida precio_venta >= precio_compra (400) además de la
  validación de Pydantic (Field(ge=0) -> 422) y el CheckConstraint de BD.
- NINGÚN endpoint de productos exige autenticación (no hay
  Depends(obtener_usuario_actual) en producto_controller.py). Esto es
  intencional documentarlo, no un supuesto a corregir aquí.
"""
import pytest


class TestProductosCRUD:
    def test_crear_producto_valido(self, client, categoria_id):
        response = client.post(
            "/api/v1/productos/",
            json={
                "nombre": "Laptop HP",
                "descripcion": "Laptop 15 pulgadas",
                "categoria_id": categoria_id,
                "precio_compra": 300.0,
                "precio_venta": 450.0,
                "unidad_medida": "unidad",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Laptop HP"
        assert "producto_id" in data

    def test_listar_productos_excluye_inactivos(self, client, producto_id):
        response = client.get("/api/v1/productos/")
        assert response.status_code == 200
        ids = [p["producto_id"] for p in response.json()]
        assert producto_id in ids

    def test_actualizar_producto_con_patch(self, client, producto_id):
        response = client.patch(
            f"/api/v1/productos/{producto_id}",
            json={"nombre": "Producto Actualizado"},
        )
        assert response.status_code == 200
        assert response.json()["nombre"] == "Producto Actualizado"

    def test_soft_delete_producto(self, client, producto_id):
        response = client.delete(f"/api/v1/productos/{producto_id}")
        assert response.status_code == 200

        # obtener_por_id no filtra por activo, así que sigue siendo consultable
        # individualmente, pero debe desaparecer del listado general.
        listado = client.get("/api/v1/productos/").json()
        ids_listado = [p["producto_id"] for p in listado]
        assert producto_id not in ids_listado


class TestProductosReglasDeNegocio:
    def test_precio_venta_menor_a_precio_compra_rechazado(self, client, categoria_id):
        """Regla de negocio en producto_service.py, distinta de la validación
        de precio negativo: aquí ambos precios son válidos (>=0) pero
        venta < compra, lo cual el service rechaza explícitamente."""
        response = client.post(
            "/api/v1/productos/",
            json={
                "nombre": "Producto Margen Invalido",
                "descripcion": "test",
                "categoria_id": categoria_id,
                "precio_compra": 100.0,
                "precio_venta": 50.0,
                "unidad_medida": "unidad",
            },
        )
        assert response.status_code == 400
        assert "precio de venta" in response.json()["detail"].lower()


class TestProductosCasosLimite:
    """Casos límite documentados en Fase 3."""

    def test_producto_inexistente_devuelve_404(self, client):
        response = client.get("/api/v1/productos/999999")
        assert response.status_code == 404

    def test_precio_negativo_rechazado_por_schema(self, client, categoria_id):
        """precio_compra/precio_venta usan Field(..., ge=0) en ProductoBase,
        así que esto se rechaza en la capa de Pydantic ANTES de llegar a
        la BD -> 422, nunca debería llegar al CheckConstraint ni dar 500."""
        response = client.post(
            "/api/v1/productos/",
            json={
                "nombre": "Producto Precio Invalido",
                "descripcion": "test",
                "categoria_id": categoria_id,
                "precio_compra": -5,
                "precio_venta": 1.0,
                "unidad_medida": "unidad",
            },
        )
        assert response.status_code == 422

    def test_precio_en_cero_permitido(self, client, categoria_id):
        """precio_compra=0 y precio_venta=0: pasa Field(ge=0) (0 es válido) y
        pasa la regla de negocio (0 no es menor que 0) -> se espera 201.
        Se documenta igual como hallazgo de negocio: ¿debería permitirse
        vender productos a precio 0?"""
        response = client.post(
            "/api/v1/productos/",
            json={
                "nombre": "Producto Cero",
                "descripcion": "test",
                "categoria_id": categoria_id,
                "precio_compra": 0,
                "precio_venta": 0,
                "unidad_medida": "unidad",
            },
        )
        print(f"[HALLAZGO] Precio en 0 -> status: {response.status_code}")
        assert response.status_code == 201

    def test_endpoint_de_productos_no_exige_token(self, client):
        """
        Hallazgo de seguridad (Fase 3): a diferencia de POST /ventas/ y
        POST /compras/, el módulo de productos completo (igual que
        usuarios, categorías, proveedores e inventario) no tiene NINGÚN
        endpoint protegido con JWT. Este test documenta el comportamiento
        actual (200 sin token), no lo valida como correcto.
        """
        response = client.get("/api/v1/productos/")
        assert response.status_code == 200
