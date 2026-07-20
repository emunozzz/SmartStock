from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import List, Optional


class DetalleVentaCreate(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0)
    precio_unitario: Decimal = Field(..., ge=0)


class VentaCreate(BaseModel):
    cliente_id: Optional[int] = None
    detalles: List[DetalleVentaCreate] = Field(..., min_length=1)


class DetalleVentaResponse(BaseModel):
    detalle_venta_id: int
    producto_id: int
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal

    model_config = ConfigDict(from_attributes=True)


class VentaResponse(BaseModel):
    venta_id: int
    cliente_id: Optional[int]
    usuario_id: int
    fecha: datetime
    total: Decimal
    estado: str
    detalles: List[DetalleVentaResponse]

    model_config = ConfigDict(from_attributes=True)