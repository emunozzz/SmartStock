from sqlalchemy.orm import Session
from app.models.proveedor_model import Proveedor
from app.models.producto_proveedor_model import ProductoProveedor
from app.schemas.proveedor_schema import ProveedorCreate, ProveedorUpdate


class ProveedorRepository:

    def __init__(self, db: Session):
        self.db = db

    def obtener_todos(self, skip: int = 0, limit: int = 100):
        return self.db.query(Proveedor).filter(Proveedor.activo == True).offset(skip).limit(limit).all()

    def obtener_por_id(self, proveedor_id: int):
        return self.db.query(Proveedor).filter(Proveedor.proveedor_id == proveedor_id).first()

    def crear(self, datos: ProveedorCreate) -> Proveedor:
        nuevo = Proveedor(**datos.model_dump())
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo

    def actualizar(self, proveedor_id: int, datos: ProveedorUpdate) -> Proveedor | None:
        proveedor = self.obtener_por_id(proveedor_id)
        if not proveedor:
            return None
        for campo, valor in datos.model_dump(exclude_unset=True).items():
            setattr(proveedor, campo, valor)
        self.db.commit()
        self.db.refresh(proveedor)
        return proveedor

    def eliminar(self, proveedor_id: int) -> bool:
        """Soft delete, mismo estándar que Producto."""
        proveedor = self.obtener_por_id(proveedor_id)
        if not proveedor:
            return False
        proveedor.activo = False
        self.db.commit()
        return True

    # --- Relación con productos (tabla intermedia) ---

    def obtener_asociacion(self, proveedor_id: int, producto_id: int):
        return self.db.query(ProductoProveedor).filter(
            ProductoProveedor.proveedor_id == proveedor_id,
            ProductoProveedor.producto_id == producto_id
        ).first()

    def asociar_producto(self, proveedor_id: int, producto_id: int, precio: float) -> ProductoProveedor:
        asociacion = ProductoProveedor(
            proveedor_id=proveedor_id,
            producto_id=producto_id,
            precio_proveedor=precio
        )
        self.db.add(asociacion)
        self.db.commit()
        self.db.refresh(asociacion)
        return asociacion

    def listar_productos_de_proveedor(self, proveedor_id: int):
        return self.db.query(ProductoProveedor).filter(
            ProductoProveedor.proveedor_id == proveedor_id
        ).all()