from sqlalchemy.orm import Session
from app.models.producto_model import Producto
from app.schemas.producto_schema import ProductoCreate, ProductoUpdate


class ProductoRepository:

    def __init__(self, db: Session):
        self.db = db

    def obtener_todos(self, skip: int = 0, limit: int = 100):
        return self.db.query(Producto).filter(Producto.activo == True).offset(skip).limit(limit).all()

    def obtener_por_id(self, producto_id: int):
        return self.db.query(Producto).filter(Producto.producto_id == producto_id).first()

    def crear(self, datos: ProductoCreate) -> Producto:
        nuevo_producto = Producto(**datos.model_dump())
        self.db.add(nuevo_producto)
        self.db.commit()
        self.db.refresh(nuevo_producto)
        return nuevo_producto

    def actualizar(self, producto_id: int, datos: ProductoUpdate) -> Producto | None:
        producto = self.obtener_por_id(producto_id)
        if not producto:
            return None
        for campo, valor in datos.model_dump(exclude_unset=True).items():
            setattr(producto, campo, valor)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def eliminar(self, producto_id: int) -> bool:
        """Eliminación lógica (soft delete): nunca se borra físicamente
        un producto con historial de compras/ventas asociado."""
        producto = self.obtener_por_id(producto_id)
        if not producto:
            return False
        producto.activo = False
        self.db.commit()
        return True