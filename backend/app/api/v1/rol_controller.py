from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.rol_service import RolService
from app.schemas.rol_schema import RolCreate, RolUpdate, RolResponse

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/", response_model=List[RolResponse])
def listar_roles(db: Session = Depends(get_db)):
    service = RolService(db)
    return service.listar_roles()


@router.get("/{rol_id}", response_model=RolResponse)
def obtener_rol(rol_id: int, db: Session = Depends(get_db)):
    service = RolService(db)
    return service.obtener_rol(rol_id)


@router.post("/", response_model=RolResponse, status_code=status.HTTP_201_CREATED)
def crear_rol(datos: RolCreate, db: Session = Depends(get_db)):
    service = RolService(db)
    return service.crear_rol(datos)


@router.patch("/{rol_id}", response_model=RolResponse)
def actualizar_rol(rol_id: int, datos: RolUpdate, db: Session = Depends(get_db)):
    service = RolService(db)
    return service.actualizar_rol(rol_id, datos)