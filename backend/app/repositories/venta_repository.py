from sqlalchemy.orm import Session, joinedload
from app.models.venta_model import Venta
from app.models.detalle_venta_model import DetalleVenta


class VentaRepository:

    def __init__(self, db: Session):
        self.db = db

    def obtener_todas(self, skip: int = 0, limit: int = 100):
        return self.db.query(Venta).options(
            joinedload(Venta.detalles)
        ).order_by(Venta.fecha.desc()).offset(skip).limit(limit).all()

    def obtener_por_id(self, venta_id: int):
        return self.db.query(Venta).options(
            joinedload(Venta.detalles)
        ).filter(Venta.venta_id == venta_id).first()

    def crear_cabecera(self, cliente_id, usuario_id: int) -> Venta:
        venta = Venta(cliente_id=cliente_id, usuario_id=usuario_id, total=0)
        self.db.add(venta)
        self.db.flush()
        return venta

    def agregar_detalle(self, venta_id: int, producto_id: int, cantidad: int, precio_unitario) -> DetalleVenta:
        subtotal = cantidad * precio_unitario
        detalle = DetalleVenta(
            venta_id=venta_id,
            producto_id=producto_id,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            subtotal=subtotal
        )
        self.db.add(detalle)
        self.db.flush()
        return detalle

    def actualizar_total(self, venta: Venta, total) -> None:
        venta.total = total
        self.db.flush()

    def obtener_mas_vendidos(self, limit: int = 10):
        """Soporte directo para el reporte 'productos mas vendidos'
        pedido en el documento original."""
        from sqlalchemy import func
        return self.db.query(
            DetalleVenta.producto_id,
            func.sum(DetalleVenta.cantidad).label("total_vendido")
        ).group_by(DetalleVenta.producto_id).order_by(
            func.sum(DetalleVenta.cantidad).desc()
        ).limit(limit).all()