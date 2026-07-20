from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.cliente_service import ClienteService
from app.schemas.cliente_schema import ClienteCreate, ClienteUpdate, ClienteResponse
from app.schemas.venta_schema import VentaResponse

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = ClienteService(db)
    return service.listar_clientes(skip, limit)


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    service = ClienteService(db)
    return service.obtener_cliente(cliente_id)


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def crear_cliente(datos: ClienteCreate, db: Session = Depends(get_db)):
    service = ClienteService(db)
    return service.crear_cliente(datos)


@router.patch("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(cliente_id: int, datos: ClienteUpdate, db: Session = Depends(get_db)):
    service = ClienteService(db)
    return service.actualizar_cliente(cliente_id, datos)


@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    service = ClienteService(db)
    return service.eliminar_cliente(cliente_id)


@router.get("/{cliente_id}/compras", response_model=List[VentaResponse])
def historial_compras(cliente_id: int, db: Session = Depends(get_db)):
    service = ClienteService(db)
    return service.obtener_historial_compras(cliente_id)