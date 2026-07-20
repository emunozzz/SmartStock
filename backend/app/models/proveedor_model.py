from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class Proveedor(Base):
    __tablename__ = "proveedores"

    proveedor_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    ruc = Column(String(30), unique=True, nullable=True)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(150), nullable=True)
    direccion = Column(String(255), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    # Relación N:M con productos, a través de producto_proveedor
    productos = relationship(
        "ProductoProveedor",
        back_populates="proveedor"
    )