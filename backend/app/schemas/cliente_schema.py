from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[str] = Field(None, max_length=150)
    direccion: Optional[str] = Field(None, max_length=255)


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=150)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[str] = Field(None, max_length=150)
    direccion: Optional[str] = Field(None, max_length=255)
    activo: Optional[bool] = None


class ClienteResponse(ClienteBase):
    cliente_id: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)