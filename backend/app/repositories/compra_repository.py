from sqlalchemy.orm import Session, joinedload
from app.models.compra_model import Compra
from app.models.detalle_compra_model import DetalleCompra


class CompraRepository:

    def __init__(self, db: Session):
        self.db = db

    def obtener_todas(self, skip: int = 0, limit: int = 100):
        return self.db.query(Compra).options(
            joinedload(Compra.detalles)
        ).order_by(Compra.fecha.desc()).offset(skip).limit(limit).all()

    def obtener_por_id(self, compra_id: int):
        return self.db.query(Compra).options(
            joinedload(Compra.detalles)
        ).filter(Compra.compra_id == compra_id).first()

    def crear_cabecera(self, proveedor_id: int, usuario_id: int) -> Compra:
        compra = Compra(proveedor_id=proveedor_id, usuario_id=usuario_id, total=0)
        self.db.add(compra)
        self.db.flush()  # asigna compra_id sin cerrar la transaccion
        return compra

    def agregar_detalle(self, compra_id: int, producto_id: int, cantidad: int, precio_unitario) -> DetalleCompra:
        subtotal = cantidad * precio_unitario
        detalle = DetalleCompra(
            compra_id=compra_id,
            producto_id=producto_id,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            subtotal=subtotal
        )
        self.db.add(detalle)
        self.db.flush()
        return detalle

    def actualizar_total(self, compra: Compra, total) -> None:
        compra.total = total
        self.db.flush()