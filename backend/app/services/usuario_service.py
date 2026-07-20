from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate
from app.core.security import hashear_contrasena


class UsuarioService:

    def __init__(self, db: Session):
        self.repository = UsuarioRepository(db)

    def listar_usuarios(self, skip: int = 0, limit: int = 100):
        return self.repository.obtener_todos(skip, limit)

    def obtener_usuario(self, usuario_id: int):
        usuario = self.repository.obtener_por_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con id {usuario_id} no encontrado"
            )
        return usuario

    def crear_usuario(self, datos: UsuarioCreate):
        existente = self.repository.obtener_por_correo(datos.correo)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario registrado con ese correo"
            )
        contrasena_hash = hashear_contrasena(datos.contrasena)
        return self.repository.crear(
            nombre=datos.nombre,
            correo=datos.correo,
            contrasena_hash=contrasena_hash,
            rol_id=datos.rol_id
        )

    def actualizar_usuario(self, usuario_id: int, datos: UsuarioUpdate):
        actualizado = self.repository.actualizar(
            usuario_id, datos.model_dump(exclude_unset=True)
        )
        if not actualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con id {usuario_id} no encontrado"
            )
        return actualizado

    def desactivar_usuario(self, usuario_id: int):
        desactivado = self.repository.desactivar(usuario_id)
        if not desactivado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con id {usuario_id} no encontrado"
            )
        return {"mensaje": "Usuario desactivado correctamente"}