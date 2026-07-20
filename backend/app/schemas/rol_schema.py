from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class RolBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=255)


class RolCreate(RolBase):
    pass


class RolUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=255)


class RolResponse(RolBase):
    rol_id: int

    model_config = ConfigDict(from_attributes=True)