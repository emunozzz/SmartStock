from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Literal


class InventarioBase(BaseModel):
    stock_minimo: int = Field(0, ge=0)
    ubicacion: Optional[str] = Field(None, max_length=100)


class InventarioCreate(InventarioBase):
    producto_id: int
    stock_actual: int = Field(0, ge=0)


class InventarioUpdate(BaseModel):
    stock_minimo: Optional[int] = Field(None, ge=0)
    ubicacion: Optional[str] = Field(None, max_length=100)


class InventarioResponse(InventarioBase):
    inventario_id: int
    producto_id: int
    stock_actual: int
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)


class MovimientoCreate(BaseModel):
    """Usado para registrar una entrada o salida manual de stock."""
    cantidad: int = Field(..., gt=0)
    motivo: Optional[str] = Field(None, max_length=255)


class MovimientoResponse(BaseModel):
    movimiento_id: int
    producto_id: int
    tipo_movimiento: Literal["entrada", "salida"]
    cantidad: int
    motivo: Optional[str]
    referencia_tipo: Optional[str]
    referencia_id: Optional[int]
    usuario_id: int
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)