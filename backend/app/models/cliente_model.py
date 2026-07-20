from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    cliente_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(150), nullable=True)
    direccion = Column(String(255), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    ventas = relationship("Venta", back_populates="cliente")