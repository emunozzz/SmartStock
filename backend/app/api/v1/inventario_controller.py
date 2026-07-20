from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.inventario_service import InventarioService
from app.schemas.inventario_schema import (
    InventarioCreate, InventarioUpdate, InventarioResponse,
    MovimientoCreate, MovimientoResponse
)

router = APIRouter(prefix="/inventario", tags=["Inventario"])


@router.get("/", response_model=List[InventarioResponse])
def listar_inventario(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = InventarioService(db)
    return service.listar_inventario(skip, limit)


@router.get("/alertas", response_model=List[InventarioResponse])
def listar_alertas_stock_bajo(db: Session = Depends(get_db)):
    """Requisito del documento original: alertas cuando el stock sea bajo."""
    service = InventarioService(db)
    return service.listar_stock_bajo()


@router.get("/{producto_id}", response_model=InventarioResponse)
def obtener_inventario(producto_id: int, db: Session = Depends(get_db)):
    service = InventarioService(db)
    return service.obtener_inventario(producto_id)


@router.post("/", response_model=InventarioResponse, status_code=status.HTTP_201_CREATED)
def crear_inventario(datos: InventarioCreate, db: Session = Depends(get_db)):
    service = InventarioService(db)
    return service.crear_inventario(datos)


@router.patch("/{producto_id}", response_model=InventarioResponse)
def actualizar_config_inventario(producto_id: int, datos: InventarioUpdate, db: Session = Depends(get_db)):
    service = InventarioService(db)
    return service.actualizar_config(producto_id, datos)


@router.get("/{producto_id}/movimientos", response_model=List[MovimientoResponse])
def listar_movimientos(producto_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = InventarioService(db)
    return service.listar_movimientos(producto_id, skip, limit)


@router.post("/{producto_id}/entradas", response_model=MovimientoResponse, status_code=status.HTTP_201_CREATED)
def registrar_entrada(
    producto_id: int, datos: MovimientoCreate,
    usuario_id: int,  # TEMPORAL: se reemplaza por el usuario autenticado (JWT) en el modulo de auth
    db: Session = Depends(get_db)
):
    service = InventarioService(db)
    return service.registrar_entrada(
        producto_id, datos.cantidad, usuario_id, datos.motivo,
        referencia_tipo="ajuste_manual"
    )


@router.post("/{producto_id}/salidas", response_model=MovimientoResponse, status_code=status.HTTP_201_CREATED)
def registrar_salida(
    producto_id: int, datos: MovimientoCreate,
    usuario_id: int,  # TEMPORAL: idem
    db: Session = Depends(get_db)
):
    service = InventarioService(db)
    return service.registrar_salida(
        producto_id, datos.cantidad, usuario_id, datos.motivo,
        referencia_tipo="ajuste_manual"
    )