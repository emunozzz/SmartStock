from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.repositories.categoria_repository import CategoriaRepository
from app.schemas.categoria_schema import CategoriaCreate, CategoriaUpdate


class CategoriaService:

    def __init__(self, db: Session):
        self.repository = CategoriaRepository(db)

    def listar_categorias(self, skip: int = 0, limit: int = 100):
        return self.repository.obtener_todas(skip, limit)

    def obtener_categoria(self, categoria_id: int):
        categoria = self.repository.obtener_por_id(categoria_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoria con id {categoria_id} no encontrada"
            )
        return categoria

    def crear_categoria(self, datos: CategoriaCreate):
        existente = self.repository.obtener_por_nombre(datos.nombre)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una categoria con el nombre '{datos.nombre}'"
            )
        return self.repository.crear(datos)

    def actualizar_categoria(self, categoria_id: int, datos: CategoriaUpdate):
        actualizada = self.repository.actualizar(categoria_id, datos)
        if not actualizada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoria con id {categoria_id} no encontrada"
            )
        return actualizada

    def eliminar_categoria(self, categoria_id: int):
        try:
            eliminada = self.repository.eliminar(categoria_id)
        except IntegrityError:
            self.repository.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar la categoria: tiene productos asociados"
            )
        if not eliminada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoria con id {categoria_id} no encontrada"
            )
        return {"mensaje": "Categoria eliminada correctamente"}