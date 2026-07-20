from sqlalchemy.orm import Session
from app.models.inventario_model import Inventario
from app.models.movimiento_model import MovimientoInventario
from app.schemas.inventario_schema import InventarioCreate, InventarioUpdate


class InventarioRepository:

    def __init__(self, db: Session):
        self.db = db

    # --- Inventario (stock actual) ---

    def obtener_todos(self, skip: int = 0, limit: int = 100):
        return self.db.query(Inventario).offset(skip).limit(limit).all()

    def obtener_por_producto(self, producto_id: int):
        return self.db.query(Inventario).filter(Inventario.producto_id == producto_id).first()

    def crear(self, datos: InventarioCreate) -> Inventario:
        nuevo = Inventario(**datos.model_dump())
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo

    def actualizar_config(self, producto_id: int, datos: InventarioUpdate):
        inventario = self.obtener_por_producto(producto_id)
        if not inventario:
            return None
        for campo, valor in datos.model_dump(exclude_unset=True).items():
            setattr(inventario, campo, valor)
        self.db.commit()
        self.db.refresh(inventario)
        return inventario

    def ajustar_stock(self, producto_id: int, delta: int) -> Inventario:
        """delta positivo = entrada, delta negativo = salida.
        No hace commit aqui: el commit lo controla el service,
        para poder combinarlo con el registro del movimiento
        en una sola transaccion atomica."""
        inventario = self.obtener_por_producto(producto_id)
        inventario.stock_actual += delta
        self.db.flush()
        return inventario

    def obtener_con_stock_bajo(self):
        return self.db.query(Inventario).filter(
            Inventario.stock_actual <= Inventario.stock_minimo
        ).all()

    # --- Movimientos (log append-only) ---

    def registrar_movimiento(
        self, producto_id: int, tipo: str, cantidad: int,
        usuario_id: int, motivo: str = None,
        referencia_tipo: str = None, referencia_id: int = None
    ) -> MovimientoInventario:
        movimiento = MovimientoInventario(
            producto_id=producto_id,
            tipo_movimiento=tipo,
            cantidad=cantidad,
            motivo=motivo,
            referencia_tipo=referencia_tipo,
            referencia_id=referencia_id,
            usuario_id=usuario_id
        )
        self.db.add(movimiento)
        self.db.flush()
        return movimiento

    def obtener_movimientos_por_producto(self, producto_id: int, skip: int = 0, limit: int = 100):
        return self.db.query(MovimientoInventario).filter(
            MovimientoInventario.producto_id == producto_id
        ).order_by(MovimientoInventario.fecha.desc()).offset(skip).limit(limit).all()