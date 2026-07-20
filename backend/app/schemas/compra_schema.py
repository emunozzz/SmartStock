from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import List


class DetalleCompraCreate(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0)
    precio_unitario: Decimal = Field(..., ge=0)


class CompraCreate(BaseModel):
    proveedor_id: int
    detalles: List[DetalleCompraCreate] = Field(..., min_length=1)


class DetalleCompraResponse(BaseModel):
    detalle_compra_id: int
    producto_id: int
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal

    model_config = ConfigDict(from_attributes=True)


class CompraResponse(BaseModel):
    compra_id: int
    proveedor_id: int
    usuario_id: int
    fecha: datetime
    total: Decimal
    estado: str
    detalles: List[DetalleCompraResponse]

    model_config = ConfigDict(from_attributes=True)