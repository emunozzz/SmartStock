from sqlalchemy.orm import Session
from app.models.rol_model import Rol
from app.schemas.rol_schema import RolCreate, RolUpdate


class RolRepository:

    def __init__(self, db: Session):
        self.db = db

    def obtener_todos(self):
        return self.db.query(Rol).all()

    def obtener_por_id(self, rol_id: int):
        return self.db.query(Rol).filter(Rol.rol_id == rol_id).first()

    def obtener_por_nombre(self, nombre: str):
        return self.db.query(Rol).filter(Rol.nombre == nombre).first()

    def crear(self, datos: RolCreate) -> Rol:
        nuevo = Rol(**datos.model_dump())
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo

    def actualizar(self, rol_id: int, datos: RolUpdate):
        rol = self.obtener_por_id(rol_id)
        if not rol:
            return None
        for campo, valor in datos.model_dump(exclude_unset=True).items():
            setattr(rol, campo, valor)
        self.db.commit()
        self.db.refresh(rol)
        return rol