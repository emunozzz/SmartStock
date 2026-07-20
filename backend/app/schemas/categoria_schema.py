from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=80)
    descripcion: Optional[str] = Field(None, max_length=255)


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=80)
    descripcion: Optional[str] = Field(None, max_length=255)


class CategoriaResponse(CategoriaBase):
    categoria_id: int

    model_config = ConfigDict(from_attributes=True)