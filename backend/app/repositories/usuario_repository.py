from sqlalchemy.orm import Session
from app.models.usuario_model import Usuario


class UsuarioRepository:

    def __init__(self, db: Session):
        self.db = db

    def obtener_todos(self, skip: int = 0, limit: int = 100):
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    def obtener_por_id(self, usuario_id: int):
        return self.db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()

    def obtener_por_correo(self, correo: str):
        return self.db.query(Usuario).filter(Usuario.correo == correo).first()

    def crear(self, nombre: str, correo: str, contrasena_hash: str, rol_id: int) -> Usuario:
        nuevo = Usuario(
            nombre=nombre,
            correo=correo,
            contrasena_hash=contrasena_hash,
            rol_id=rol_id
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo

    def actualizar(self, usuario_id: int, datos: dict):
        usuario = self.obtener_por_id(usuario_id)
        if not usuario:
            return None
        for campo, valor in datos.items():
            setattr(usuario, campo, valor)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def desactivar(self, usuario_id: int) -> bool:
        usuario = self.obtener_por_id(usuario_id)
        if not usuario:
            return False
        usuario.activo = False
        self.db.commit()
        return True