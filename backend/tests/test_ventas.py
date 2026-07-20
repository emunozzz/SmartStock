"""
Tests del módulo de ventas.

Revisado contra venta_service.py / compra_service.py / inventario_repository.py:
- POST /ventas/ y POST /compras/ SÍ exigen JWT (Depends(obtener_usuario_actual)).
  Son los únicos endpoints protegidos en todo el backend.
- ajustar_stock() asume que ya existe un registro de Inventario para el
  producto; si no existe, lanza AttributeError -> 500 (bug real, ver test
  dedicado más abajo). Por eso el fixture crea el inventario explícitamente
  antes de comprar.
"""
import pytest


@pytest.fixture()
def producto_con_stock(client, admin_headers, producto_con_inventario):
    """
    Registra una compra de 50 unidades sobre un producto que YA tiene
    registro de inventario (stock_actual=0 inicial), dejándolo en 50.
    """
    producto_id = producto_con_inventario

    proveedor_response = client.post(
        "/api/v1/proveedores/",
        json={"nombre": "Proveedor Test"},
    )
    assert proveedor_response.status_code == 201, f"No se pudo crear proveedor: {proveedor_response.text}"
    proveedor_id = proveedor_response.json()["proveedor_id"]

    compra_response = client.post(
        "/api/v1/compras/",
        json={
            "proveedor_id": proveedor_id,
            "detalles": [
                {"producto_id": producto_id, "cantidad": 50, "precio_unitario": 5.0}
            ],
        },
        headers=admin_headers,
    )
    assert compra_response.status_code == 201, f"Compra falló: {compra_response.text}"
    return producto_id


class TestVentasFlujoNormal:
    def test_venta_reduce_stock(self, client, admin_headers, producto_con_stock):
        producto_id = producto_con_stock

        response = client.post(
            "/api/v1/ventas/",
            json={
                "detalles": [
                    {"producto_id": producto_id, "cantidad": 10, "precio_unitario": 8.0}
                ]
            },
            headers=admin_headers,
        )
        assert response.status_code == 201

        inventario_response = client.get(f"/api/v1/inventario/{producto_id}")
        assert inventario_response.status_code == 200
        # 50 (compra) - 10 (venta) = 40
        assert inventario_response.json()["stock_actual"] == 40


class TestVentasCasosLimite:
    """Caso límite documentado en Fase 3."""

    def test_venta_supera_stock_disponible(self, client, admin_headers, producto_con_stock):
        producto_id = producto_con_stock

        response = client.post(
            "/api/v1/ventas/",
            json={
                "detalles": [
                    {"producto_id": producto_id, "cantidad": 9999, "precio_unitario": 1.0}
                ]
            },
            headers=admin_headers,
        )
        # Confirmado en venta_service.py: verifica stock ANTES de tocar nada
        # y lanza HTTPException 400 explícita. No debería dar 500.
        assert response.status_code == 400
        assert "stock insuficiente" in response.json()["detail"].lower()

    def test_venta_sin_token_rechazada(self, client, producto_con_stock):
        """POST /ventas/ es uno de los dos únicos endpoints con JWT obligatorio."""
        producto_id = producto_con_stock
        response = client.post(
            "/api/v1/ventas/",
            json={
                "detalles": [
                    {"producto_id": producto_id, "cantidad": 1, "precio_unitario": 1.0}
                ]
            },
            # sin headers de Authorization
        )
        assert response.status_code == 401


class TestComprasSinInventarioPrevio:
    """
    Hallazgo de Fase 3/4: comprar un producto que NUNCA tuvo un registro
    de inventario (sin pasar por POST /api/v1/inventario/ primero) provoca
    un 500 en vez de un error controlado, porque ajustar_stock() asume
    que el registro ya existe.
    """

    def test_comprar_producto_sin_inventario_previo_da_500(
        self, client, admin_headers, producto_id
    ):
        # OJO: aquí usamos `producto_id` (sin inventario creado), no
        # `producto_con_inventario`, a propósito -- para reproducir el bug.
        proveedor_response = client.post(
            "/api/v1/proveedores/", json={"nombre": "Proveedor Sin Inventario"}
        )
        proveedor_id = proveedor_response.json()["proveedor_id"]

        response = client.post(
            "/api/v1/compras/",
            json={
                "proveedor_id": proveedor_id,
                "detalles": [
                    {"producto_id": producto_id, "cantidad": 10, "precio_unitario": 5.0}
                ],
            },
            headers=admin_headers,
        )
        # Comportamiento actual documentado como bug -- lo ideal sería 404 o 400
        # ("el producto no tiene inventario inicializado"), no 500.
        print(f"[BUG DOCUMENTADO] Compra sin inventario previo -> status: {response.status_code}")
        assert response.status_code == 500
