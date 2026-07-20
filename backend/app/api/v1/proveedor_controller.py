from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.proveedor_service import ProveedorService
from app.schemas.proveedor_schema import (
    ProveedorCreate, ProveedorUpdate, ProveedorResponse,
    AsociarProductoProveedor, ProductoDeProveedorResponse
)

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


@router.get("/", response_model=List[ProveedorResponse])
def listar_proveedores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = ProveedorService(db)
    return service.listar_proveedores(skip, limit)


@router.get("/{proveedor_id}", response_model=ProveedorResponse)
def obtener_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    service = ProveedorService(db)
    return service.obtener_proveedor(proveedor_id)


@router.post("/", response_model=ProveedorResponse, status_code=status.HTTP_201_CREATED)
def crear_proveedor(datos: ProveedorCreate, db: Session = Depends(get_db)):
    service = ProveedorService(db)
    return service.crear_proveedor(datos)


@router.patch("/{proveedor_id}", response_model=ProveedorResponse)
def actualizar_proveedor(proveedor_id: int, datos: ProveedorUpdate, db: Session = Depends(get_db)):
    service = ProveedorService(db)
    return service.actualizar_proveedor(proveedor_id, datos)


@router.delete("/{proveedor_id}")
def eliminar_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    service = ProveedorService(db)
    return service.eliminar_proveedor(proveedor_id)


@router.post(
    "/{proveedor_id}/productos",
    response_model=ProductoDeProveedorResponse,
    status_code=status.HTTP_201_CREATED
)
def asociar_producto(proveedor_id: int, datos: AsociarProductoProveedor, db: Session = Depends(get_db)):
    service = ProveedorService(db)
    return service.asociar_producto(proveedor_id, datos)


@router.get("/{proveedor_id}/productos", response_model=List[ProductoDeProveedorResponse])
def listar_productos_de_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    service = ProveedorService(db)
    return service.listar_productos_de_proveedor(proveedor_id)