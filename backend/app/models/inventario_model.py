from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Inventario(Base):
    __tablename__ = "inventario"

    inventario_id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(
        Integer, ForeignKey("productos.producto_id"), unique=True, nullable=False
    )
    stock_actual = Column(Integer, nullable=False, default=0)
    stock_minimo = Column(Integer, nullable=False, default=0)
    ubicacion = Column(String(100), nullable=True)
    fecha_actualizacion = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    producto = relationship("Producto", backref="inventario", uselist=False)