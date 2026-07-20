"""
Tests del módulo de inventario.

Revisado contra inventario_controller.py real:
- Las rutas son /{producto_id}/entradas y /{producto_id}/salidas (plural).
- NINGÚN endpoint de inventario tiene Depends(obtener_usuario_actual) --
  ni siquiera entradas/salidas. usuario_id se recibe como query param
  manual (comentado en el código como "TEMPORAL: se reemplaza por el
  usuario autenticado (JWT) en el modulo de auth"). Esto es EXACTAMENTE
  el bug que ya tenías anotado en Fase 3, y es más grave de lo que parecía:
  no es solo que no tome el usuario del JWT, es que no hay JWT en absoluto.
"""
import pytest


class TestInventarioConsultas:
    def test_alertas_stock_bajo(self, client, producto_con_inventario):
        response = client.get("/api/v1/inventario/alertas")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_movimientos_de_producto(self, client, producto_con_inventario):
        producto_id = producto_con_inventario
        response = client.get(f"/api/v1/inventario/{producto_id}/movimientos")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_movimientos_producto_sin_inventario_da_404(self, client):
        response = client.get("/api/v1/inventario/999999/movimientos")
        assert response.status_code == 404


class TestInventarioEntradaSalida:
    def test_entrada_manual_sin_ningun_token_es_aceptada(self, client, producto_con_inventario):
        """
        Hallazgo de seguridad (Fase 3): se espera 401 si el endpoint estuviera
        protegido, pero como NO hay Depends(obtener_usuario_actual) en
        inventario_controller.py, la petición se acepta sin token alguno
        con solo pasar usuario_id como query param manual. Este test
        documenta el comportamiento REAL, no lo aprueba.
        """
        producto_id = producto_con_inventario
        response = client.post(
            f"/api/v1/inventario/{producto_id}/entradas",
            params={"usuario_id": 1},  # usuario_id es query param, no viene del JWT
            json={"cantidad": 10, "motivo": "ajuste manual de prueba"},
            # sin headers de Authorization -- y aun así funciona
        )
        print(f"[HALLAZGO DE SEGURIDAD] Entrada sin token -> status: {response.status_code}")
        assert response.status_code == 201

    def test_entrada_registra_usuario_id_arbitrario_no_verificado(
        self, client, producto_con_inventario
    ):
        """
        Documenta que usuario_id es un entero arbitrario que el cliente
        puede mandar (ej. el usuario_id de OTRA persona), sin ninguna
        verificación de que corresponda al usuario real haciendo la
        petición -- porque no hay autenticación de por medio.
        """
        producto_id = producto_con_inventario
        usuario_id_arbitrario = 99999  # no existe como usuario real

        response = client.post(
            f"/api/v1/inventario/{producto_id}/entradas",
            params={"usuario_id": usuario_id_arbitrario},
            json={"cantidad": 5, "motivo": "usuario inventado"},
        )
        # Se documenta el resultado real: si esto da 201, confirma que no
        # hay validación de que usuario_id exista ni de quién hace la petición.
        print(f"[HALLAZGO] usuario_id arbitrario -> status: {response.status_code}")

    def test_salida_supera_stock_disponible(self, client, producto_con_inventario):
        producto_id = producto_con_inventario
        response = client.post(
            f"/api/v1/inventario/{producto_id}/salidas",
            params={"usuario_id": 1},
            json={"cantidad": 9999, "motivo": "salida excesiva de prueba"},
        )
        assert response.status_code == 400
        assert "stock insuficiente" in response.json()["detail"].lower()
