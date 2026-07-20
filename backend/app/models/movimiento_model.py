from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"
    __table_args__ = (
        CheckConstraint("tipo_movimiento IN ('entrada', 'salida')", name="ck_tipo_movimiento"),
        CheckConstraint("cantidad > 0", name="ck_cantidad_positiva"),
    )

    movimiento_id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.producto_id"), nullable=False)
    tipo_movimiento = Column(String(10), nullable=False)
    cantidad = Column(Integer, nullable=False)
    motivo = Column(String(255), nullable=True)
    referencia_tipo = Column(String(20), nullable=True)
    referencia_id = Column(Integer, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())

    producto = relationship("Producto", backref="movimientos")