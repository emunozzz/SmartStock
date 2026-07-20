from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.venta_service import VentaService
from app.schemas.venta_schema import VentaCreate, VentaResponse
from app.middlewares.auth_middleware import obtener_usuario_actual
from app.models.usuario_model import Usuario

router = APIRouter(prefix="/ventas", tags=["Ventas"])


@router.get("/", response_model=List[VentaResponse])
def listar_ventas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = VentaService(db)
    return service.listar_ventas(skip, limit)


@router.get("/{venta_id}", response_model=VentaResponse)
def obtener_venta(venta_id: int, db: Session = Depends(get_db)):
    service = VentaService(db)
    return service.obtener_venta(venta_id)


@router.post("/", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
def registrar_venta(
    datos: VentaCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    service = VentaService(db)
    return service.registrar_venta(datos, usuario_actual.usuario_id)