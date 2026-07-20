from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional, List


class ProveedorBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    ruc: Optional[str] = Field(None, max_length=30)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[str] = Field(None, max_length=150)
    direccion: Optional[str] = Field(None, max_length=255)


class ProveedorCreate(ProveedorBase):
    pass


class ProveedorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=150)
    ruc: Optional[str] = Field(None, max_length=30)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[str] = Field(None, max_length=150)
    direccion: Optional[str] = Field(None, max_length=255)
    activo: Optional[bool] = None


class ProveedorResponse(ProveedorBase):
    proveedor_id: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)


class AsociarProductoProveedor(BaseModel):
    """Usado para vincular un producto existente a un proveedor con su precio."""
    producto_id: int
    precio_proveedor: Decimal = Field(..., ge=0)


class ProductoDeProveedorResponse(BaseModel):
    producto_id: int
    precio_proveedor: Decimal

    model_config = ConfigDict(from_attributes=True)