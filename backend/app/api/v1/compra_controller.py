from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.compra_service import CompraService
from app.schemas.compra_schema import CompraCreate, CompraResponse
from app.middlewares.auth_middleware import obtener_usuario_actual
from app.models.usuario_model import Usuario

router = APIRouter(prefix="/compras", tags=["Compras"])


@router.get("/", response_model=List[CompraResponse])
def listar_compras(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = CompraService(db)
    return service.listar_compras(skip, limit)


@router.get("/{compra_id}", response_model=CompraResponse)
def obtener_compra(compra_id: int, db: Session = Depends(get_db)):
    service = CompraService(db)
    return service.obtener_compra(compra_id)


@router.post("/", response_model=CompraResponse, status_code=status.HTTP_201_CREATED)
def registrar_compra(
    datos: CompraCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    service = CompraService(db)
    return service.registrar_compra(datos, usuario_actual.usuario_id)