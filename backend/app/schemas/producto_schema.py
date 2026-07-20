from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import Optional


class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    descripcion: Optional[str] = Field(None, max_length=255)
    categoria_id: int
    precio_compra: Decimal = Field(..., ge=0)
    precio_venta: Decimal = Field(..., ge=0)
    unidad_medida: str = Field(..., max_length=20)


class ProductoCreate(ProductoBase):
    """Datos requeridos para crear un producto (POST)."""
    pass


class ProductoUpdate(BaseModel):
    """Todos los campos opcionales: permite actualizaciones parciales (PATCH)."""
    nombre: Optional[str] = Field(None, min_length=1, max_length=150)
    descripcion: Optional[str] = Field(None, max_length=255)
    categoria_id: Optional[int] = None
    precio_compra: Optional[Decimal] = Field(None, ge=0)
    precio_venta: Optional[Decimal] = Field(None, ge=0)
    unidad_medida: Optional[str] = Field(None, max_length=20)
    activo: Optional[bool] = None


class ProductoResponse(ProductoBase):
    """Lo que la API devuelve al cliente."""
    producto_id: int
    activo: bool
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)