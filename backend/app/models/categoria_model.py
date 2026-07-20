from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    categoria_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(80), unique=True, nullable=False, index=True)
    descripcion = Column(String(255), nullable=True)

    # Relación con productos (definida en producto_model.py)
    productos = relationship("Producto", back_populates="categoria")