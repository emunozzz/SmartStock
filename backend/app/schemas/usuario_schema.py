from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional


class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    correo: EmailStr
    rol_id: int


class UsuarioCreate(UsuarioBase):
    contrasena: str = Field(..., min_length=8, max_length=100)


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    rol_id: Optional[int] = None
    activo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    usuario_id: int
    activo: bool
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)