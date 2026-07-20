from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Compra(Base):
    __tablename__ = "compras"

    compra_id = Column(Integer, primary_key=True, index=True)
    proveedor_id = Column(Integer, ForeignKey("proveedores.proveedor_id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    total = Column(Numeric(10, 2), nullable=False, default=0)
    estado = Column(String(20), nullable=False, default="completada")

    proveedor = relationship("Proveedor", backref="compras")
    usuario = relationship("Usuario", backref="compras")
    detalles = relationship(
        "DetalleCompra", back_populates="compra", cascade="all, delete-orphan"
    )