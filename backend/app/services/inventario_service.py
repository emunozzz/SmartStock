from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.inventario_repository import InventarioRepository
from app.schemas.inventario_schema import InventarioCreate, InventarioUpdate


class InventarioService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = InventarioRepository(db)

    def listar_inventario(self, skip: int = 0, limit: int = 100):
        return self.repository.obtener_todos(skip, limit)

    def obtener_inventario(self, producto_id: int):
        inventario = self.repository.obtener_por_producto(producto_id)
        if not inventario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe registro de inventario para el producto {producto_id}"
            )
        return inventario

    def crear_inventario(self, datos: InventarioCreate):
        existente = self.repository.obtener_por_producto(datos.producto_id)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El producto {datos.producto_id} ya tiene un registro de inventario"
            )
        return self.repository.crear(datos)

    def actualizar_config(self, producto_id: int, datos: InventarioUpdate):
        actualizado = self.repository.actualizar_config(producto_id, datos)
        if not actualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe registro de inventario para el producto {producto_id}"
            )
        return actualizado

    def listar_stock_bajo(self):
        """Cumple el requisito de 'alertas de stock bajo' del documento original."""
        return self.repository.obtener_con_stock_bajo()

    def listar_movimientos(self, producto_id: int, skip: int = 0, limit: int = 100):
        self.obtener_inventario(producto_id)  # valida que exista
        return self.repository.obtener_movimientos_por_producto(producto_id, skip, limit)

    # --- Operaciones centrales, reutilizables por Compras y Ventas ---

    def verificar_stock_suficiente(self, producto_id: int, cantidad: int) -> bool:
        inventario = self.obtener_inventario(producto_id)
        return inventario.stock_actual >= cantidad

    def registrar_entrada(
        self, producto_id: int, cantidad: int, usuario_id: int,
        motivo: str = None, referencia_tipo: str = None, referencia_id: int = None
    ):
        self.obtener_inventario(producto_id)  # valida que exista, lanza 404 si no
        try:
            self.repository.ajustar_stock(producto_id, delta=cantidad)
            movimiento = self.repository.registrar_movimiento(
                producto_id, "entrada", cantidad, usuario_id,
                motivo, referencia_tipo, referencia_id
            )
            self.db.commit()
            self.db.refresh(movimiento)
            return movimiento
        except Exception:
            self.db.rollback()
            raise

    def registrar_salida(
        self, producto_id: int, cantidad: int, usuario_id: int,
        motivo: str = None, referencia_tipo: str = None, referencia_id: int = None
    ):
        if not self.verificar_stock_suficiente(producto_id, cantidad):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para el producto {producto_id}"
            )
        try:
            self.repository.ajustar_stock(producto_id, delta=-cantidad)
            movimiento = self.repository.registrar_movimiento(
                producto_id, "salida", cantidad, usuario_id,
                motivo, referencia_tipo, referencia_id
            )
            self.db.commit()
            self.db.refresh(movimiento)
            return movimiento
        except Exception:
            self.db.rollback()
            raise