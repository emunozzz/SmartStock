from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.rol_repository import RolRepository
from app.schemas.rol_schema import RolCreate, RolUpdate


class RolService:

    def __init__(self, db: Session):
        self.repository = RolRepository(db)

    def listar_roles(self):
        return self.repository.obtener_todos()

    def obtener_rol(self, rol_id: int):
        rol = self.repository.obtener_por_id(rol_id)
        if not rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rol con id {rol_id} no encontrado"
            )
        return rol

    def crear_rol(self, datos: RolCreate):
        existente = self.repository.obtener_por_nombre(datos.nombre)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un rol con el nombre '{datos.nombre}'"
            )
        return self.repository.crear(datos)

    def actualizar_rol(self, rol_id: int, datos: RolUpdate):
        actualizado = self.repository.actualizar(rol_id, datos)
        if not actualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rol con id {rol_id} no encontrado"
            )
        return actualizado