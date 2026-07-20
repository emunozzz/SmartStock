from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.proveedor_repository import ProveedorRepository
from app.schemas.proveedor_schema import ProveedorCreate, ProveedorUpdate, AsociarProductoProveedor


class ProveedorService:

    def __init__(self, db: Session):
        self.repository = ProveedorRepository(db)

    def listar_proveedores(self, skip: int = 0, limit: int = 100):
        return self.repository.obtener_todos(skip, limit)

    def obtener_proveedor(self, proveedor_id: int):
        proveedor = self.repository.obtener_por_id(proveedor_id)
        if not proveedor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor con id {proveedor_id} no encontrado"
            )
        return proveedor

    def crear_proveedor(self, datos: ProveedorCreate):
        return self.repository.crear(datos)

    def actualizar_proveedor(self, proveedor_id: int, datos: ProveedorUpdate):
        actualizado = self.repository.actualizar(proveedor_id, datos)
        if not actualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor con id {proveedor_id} no encontrado"
            )
        return actualizado

    def eliminar_proveedor(self, proveedor_id: int):
        eliminado = self.repository.eliminar(proveedor_id)
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor con id {proveedor_id} no encontrado"
            )
        return {"mensaje": "Proveedor eliminado correctamente"}

    def asociar_producto(self, proveedor_id: int, datos: AsociarProductoProveedor):
        self.obtener_proveedor(proveedor_id)  # valida que el proveedor exista (lanza 404 si no)

        existente = self.repository.obtener_asociacion(proveedor_id, datos.producto_id)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este producto ya está asociado a este proveedor"
            )

        return self.repository.asociar_producto(
            proveedor_id, datos.producto_id, datos.precio_proveedor
        )

    def listar_productos_de_proveedor(self, proveedor_id: int):
        self.obtener_proveedor(proveedor_id)
        return self.repository.listar_productos_de_proveedor(proveedor_id)