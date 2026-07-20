from sqlalchemy import Column, Integer, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class DetalleCompra(Base):
    __tablename__ = "detalle_compra"
    __table_args__ = (
        CheckConstraint("cantidad > 0", name="ck_detalle_compra_cantidad_positiva"),
    )

    detalle_compra_id = Column(Integer, primary_key=True, index=True)
    compra_id = Column(Integer, ForeignKey("compras.compra_id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.producto_id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    compra = relationship("Compra", back_populates="detalles")
    producto = relationship("Producto", backref="detalles_compra")