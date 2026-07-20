from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.producto_service import ProductoService
from app.schemas.producto_schema import ProductoCreate, ProductoUpdate, ProductoResponse

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/", response_model=List[ProductoResponse])
def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = ProductoService(db)
    return service.listar_productos(skip, limit)


@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    service = ProductoService(db)
    return service.obtener_producto(producto_id)


@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(datos: ProductoCreate, db: Session = Depends(get_db)):
    service = ProductoService(db)
    return service.crear_producto(datos)


@router.patch("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: int, datos: ProductoUpdate, db: Session = Depends(get_db)):
    service = ProductoService(db)
    return service.actualizar_producto(producto_id, datos)


@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    service = ProductoService(db)
    return service.eliminar_producto(producto_id)