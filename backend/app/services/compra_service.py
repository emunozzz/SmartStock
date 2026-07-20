from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.compra_repository import CompraRepository
from app.services.inventario_service import InventarioService
from app.schemas.compra_schema import CompraCreate


class CompraService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = CompraRepository(db)
        self.inventario_service = InventarioService(db)

    def listar_compras(self, skip: int = 0, limit: int = 100):
        return self.repository.obtener_todas(skip, limit)

    def obtener_compra(self, compra_id: int):
        compra = self.repository.obtener_por_id(compra_id)
        if not compra:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compra con id {compra_id} no encontrada"
            )
        return compra

    def registrar_compra(self, datos: CompraCreate, usuario_id: int):
        try:
            compra = self.repository.crear_cabecera(datos.proveedor_id, usuario_id)

            total_acumulado = 0
            for linea in datos.detalles:
                detalle = self.repository.agregar_detalle(
                    compra.compra_id, linea.producto_id,
                    linea.cantidad, linea.precio_unitario
                )
                total_acumulado += detalle.subtotal

                # Cada linea de compra aumenta el stock del producto correspondiente.
                # Reutilizamos InventarioService en vez de duplicar la logica de stock.
                self.inventario_service.repository.ajustar_stock(
                    linea.producto_id, delta=linea.cantidad
                )
                self.inventario_service.repository.registrar_movimiento(
                    linea.producto_id, "entrada", linea.cantidad, usuario_id,
                    motivo="Compra a proveedor",
                    referencia_tipo="compra", referencia_id=compra.compra_id
                )

            self.repository.actualizar_total(compra, total_acumulado)
            self.db.commit()
            self.db.refresh(compra)
            return compra

        except Exception:
            self.db.rollback()
            raise