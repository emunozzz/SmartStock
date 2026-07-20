from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente_schema import ClienteCreate, ClienteUpdate


class ClienteService:

    def __init__(self, db: Session):
        self.repository = ClienteRepository(db)

    def listar_clientes(self, skip: int = 0, limit: int = 100):
        return self.repository.obtener_todos(skip, limit)

    def obtener_cliente(self, cliente_id: int):
        cliente = self.repository.obtener_por_id(cliente_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con id {cliente_id} no encontrado"
            )
        return cliente

    def crear_cliente(self, datos: ClienteCreate):
        return self.repository.crear(datos)

    def actualizar_cliente(self, cliente_id: int, datos: ClienteUpdate):
        actualizado = self.repository.actualizar(cliente_id, datos)
        if not actualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con id {cliente_id} no encontrado"
            )
        return actualizado

    def eliminar_cliente(self, cliente_id: int):
        eliminado = self.repository.eliminar(cliente_id)
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con id {cliente_id} no encontrado"
            )
        return {"mensaje": "Cliente eliminado correctamente"}

    def obtener_historial_compras(self, cliente_id: int):
        historial = self.repository.obtener_historial_compras(cliente_id)
        if historial is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con id {cliente_id} no encontrado"
            )
        return historial