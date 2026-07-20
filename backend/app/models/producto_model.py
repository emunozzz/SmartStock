from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Boolean,
    ForeignKey,
    DateTime,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Producto(Base):
    __tablename__ = "productos"

    __table_args__ = (
        CheckConstraint(
            "precio_compra >= 0",
            name="ck_precio_compra_no_negativo",
        ),
        CheckConstraint(
            "precio_venta >= 0",
            name="ck_precio_venta_no_negativo",
        ),
    )

    producto_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(String(255), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.categoria_id"), nullable=False)
    precio_compra = Column(Numeric(10, 2), nullable=False)
    precio_venta = Column(Numeric(10, 2), nullable=False)
    unidad_medida = Column(String(20), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # Relación con categoria (definida más abajo, en categoria_model.py)
    categoria = relationship("Categoria", back_populates="productos")