from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.core.database import Base


class ProductoProveedor(Base):
    __tablename__ = "producto_proveedor"

    producto_id = Column(
        Integer, ForeignKey("productos.producto_id"), primary_key=True
    )
    proveedor_id = Column(
        Integer, ForeignKey("proveedores.proveedor_id"), primary_key=True
    )
    precio_proveedor = Column(Numeric(10, 2), nullable=False)

    producto = relationship("Producto", backref="proveedores_asociados")
    proveedor = relationship("Proveedor", back_populates="productos")