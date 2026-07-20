from sqlalchemy.orm import Session
from app.models.cliente_model import Cliente
from app.schemas.cliente_schema import ClienteCreate, ClienteUpdate


class ClienteRepository:

    def __init__(self, db: Session):
        self.db = db

    def obtener_todos(self, skip: int = 0, limit: int = 100):
        return self.db.query(Cliente).filter(Cliente.activo == True).offset(skip).limit(limit).all()

    def obtener_por_id(self, cliente_id: int):
        return self.db.query(Cliente).filter(Cliente.cliente_id == cliente_id).first()

    def crear(self, datos: ClienteCreate) -> Cliente:
        nuevo = Cliente(**datos.model_dump())
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo

    def actualizar(self, cliente_id: int, datos: ClienteUpdate) -> Cliente | None:
        cliente = self.obtener_por_id(cliente_id)
        if not cliente:
            return None
        for campo, valor in datos.model_dump(exclude_unset=True).items():
            setattr(cliente, campo, valor)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def eliminar(self, cliente_id: int) -> bool:
        """Soft delete, mismo estándar del proyecto."""
        cliente = self.obtener_por_id(cliente_id)
        if not cliente:
            return False
        cliente.activo = False
        self.db.commit()
        return True

    def obtener_historial_compras(self, cliente_id: int):
        """
        Recorre la relación cliente -> ventas -> detalles,
        aprovechando el ORM en vez de escribir SQL manual.
        """
        cliente = self.obtener_por_id(cliente_id)
        if not cliente:
            return None
        return cliente.ventas