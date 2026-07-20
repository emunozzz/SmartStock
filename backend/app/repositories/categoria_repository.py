from sqlalchemy.orm import Session
from app.models.categoria_model import Categoria
from app.schemas.categoria_schema import CategoriaCreate, CategoriaUpdate


class CategoriaRepository:

    def __init__(self, db: Session):
        self.db = db

    def obtener_todas(self, skip: int = 0, limit: int = 100):
        return self.db.query(Categoria).offset(skip).limit(limit).all()

    def obtener_por_id(self, categoria_id: int):
        return self.db.query(Categoria).filter(Categoria.categoria_id == categoria_id).first()

    def obtener_por_nombre(self, nombre: str):
        return self.db.query(Categoria).filter(Categoria.nombre == nombre).first()

    def crear(self, datos: CategoriaCreate) -> Categoria:
        nueva = Categoria(**datos.model_dump())
        self.db.add(nueva)
        self.db.commit()
        self.db.refresh(nueva)
        return nueva

    def actualizar(self, categoria_id: int, datos: CategoriaUpdate) -> Categoria | None:
        categoria = self.obtener_por_id(categoria_id)
        if not categoria:
            return None
        for campo, valor in datos.model_dump(exclude_unset=True).items():
            setattr(categoria, campo, valor)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def eliminar(self, categoria_id: int) -> bool:
        categoria = self.obtener_por_id(categoria_id)
        if not categoria:
            return False
        self.db.delete(categoria)
        self.db.commit()
        return True