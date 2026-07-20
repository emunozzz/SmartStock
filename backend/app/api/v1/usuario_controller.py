from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.usuario_service import UsuarioService
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = UsuarioService(db)
    return service.listar_usuarios(skip, limit)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    service = UsuarioService(db)
    return service.obtener_usuario(usuario_id)


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):
    service = UsuarioService(db)
    return service.crear_usuario(datos)


@router.patch("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: int, datos: UsuarioUpdate, db: Session = Depends(get_db)):
    service = UsuarioService(db)
    return service.actualizar_usuario(usuario_id, datos)


@router.delete("/{usuario_id}")
def desactivar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    service = UsuarioService(db)
    return service.desactivar_usuario(usuario_id)