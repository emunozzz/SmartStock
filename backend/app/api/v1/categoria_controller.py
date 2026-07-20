from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.categoria_service import CategoriaService
from app.schemas.categoria_schema import CategoriaCreate, CategoriaUpdate, CategoriaResponse

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get("/", response_model=List[CategoriaResponse])
def listar_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = CategoriaService(db)
    return service.listar_categorias(skip, limit)


@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    service = CategoriaService(db)
    return service.obtener_categoria(categoria_id)


@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def crear_categoria(datos: CategoriaCreate, db: Session = Depends(get_db)):
    service = CategoriaService(db)
    return service.crear_categoria(datos)


@router.patch("/{categoria_id}", response_model=CategoriaResponse)
def actualizar_categoria(categoria_id: int, datos: CategoriaUpdate, db: Session = Depends(get_db)):
    service = CategoriaService(db)
    return service.actualizar_categoria(categoria_id, datos)


@router.delete("/{categoria_id}")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    service = CategoriaService(db)
    return service.eliminar_categoria(categoria_id)