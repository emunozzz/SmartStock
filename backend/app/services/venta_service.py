from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.venta_repository import VentaRepository
from app.services.inventario_service import InventarioService
from app.schemas.venta_schema import VentaCreate


class VentaService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = VentaRepository(db)
        self.inventario_service = InventarioService(db)

    def listar_ventas(self, skip: int = 0, limit: int = 100):
        return self.repository.obtener_todas(skip, limit)

    def obtener_venta(self, venta_id: int):
        venta = self.repository.obtener_por_id(venta_id)
        if not venta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Venta con id {venta_id} no encontrada"
            )
        return venta

    def registrar_venta(self, datos: VentaCreate, usuario_id: int):
        # Paso 1: verificar stock de TODAS las lineas antes de tocar nada.
        # Esto evita registrar una venta parcial si la linea 3 de 5 no tiene stock.
        for linea in datos.detalles:
            if not self.inventario_service.verificar_stock_suficiente(linea.producto_id, linea.cantidad):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuficiente para el producto {linea.producto_id}"
                )

        # Paso 2: con el stock confirmado, registrar la venta completa.
        try:
            venta = self.repository.crear_cabecera(datos.cliente_id, usuario_id)

            total_acumulado = 0
            for linea in datos.detalles:
                detalle = self.repository.agregar_detalle(
                    venta.venta_id, linea.producto_id,
                    linea.cantidad, linea.precio_unitario
                )
                total_acumulado += detalle.subtotal

                self.inventario_service.repository.ajustar_stock(
                    linea.producto_id, delta=-linea.cantidad
                )
                self.inventario_service.repository.registrar_movimiento(
                    linea.producto_id, "salida", linea.cantidad, usuario_id,
                    motivo="Venta a cliente",
                    referencia_tipo="venta", referencia_id=venta.venta_id
                )

            self.repository.actualizar_total(venta, total_acumulado)
            self.db.commit()
            self.db.refresh(venta)
            return venta

        except Exception:
            self.db.rollback()
            raise