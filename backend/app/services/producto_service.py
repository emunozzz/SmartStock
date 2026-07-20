from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.producto_repository import ProductoRepository
from app.schemas.producto_schema import ProductoCreate, ProductoUpdate


class ProductoService:

    def __init__(self, db: Session):
        self.repository = ProductoRepository(db)

    def listar_productos(self, skip: int = 0, limit: int = 100):
        return self.repository.obtener_todos(skip, limit)

    def obtener_producto(self, producto_id: int):
        producto = self.repository.obtener_por_id(producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id {producto_id} no encontrado"
            )
        return producto

    def crear_producto(self, datos: ProductoCreate):
        if datos.precio_venta < datos.precio_compra:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio de venta no puede ser menor al precio de compra"
            )
        return self.repository.crear(datos)

    def actualizar_producto(self, producto_id: int, datos: ProductoUpdate):
        producto_actualizado = self.repository.actualizar(producto_id, datos)
        if not producto_actualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id {producto_id} no encontrado"
            )
        return producto_actualizado

    def eliminar_producto(self, producto_id: int):
        eliminado = self.repository.eliminar(producto_id)
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id {producto_id} no encontrado"
            )
        return {"mensaje": "Producto eliminado correctamente"}