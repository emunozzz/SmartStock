"""
seed_admin.py — Crea un usuario administrador por defecto para SmartStock.

USO:
    python -m script.seed_admin
"""
import sys
from app.core.database import SessionLocal
from app.core.security import hashear_contrasena
from app.models.rol_model import Rol
from app.models.usuario_model import Usuario

CORREO_ADMIN = "admin@smartstock.com"
CONTRASENA_ADMIN = "admin123"


def main():
    db = SessionLocal()
    try:
        rol = db.query(Rol).filter(Rol.nombre == "admin").first()
        if not rol:
            rol = Rol(nombre="admin", descripcion="Administrador del sistema")
            db.add(rol)
            db.flush()
            print("Rol 'admin' creado.")

        usuario = db.query(Usuario).filter(Usuario.correo == CORREO_ADMIN).first()
        if usuario:
            print(f"El usuario {CORREO_ADMIN} ya existe. No se crea duplicado.")
            return

        usuario = Usuario(
            nombre="Administrador",
            correo=CORREO_ADMIN,
            contrasena_hash=hashear_contrasena(CONTRASENA_ADMIN),
            rol_id=rol.rol_id,
            activo=True,
        )
        db.add(usuario)
        db.commit()

        print(f"\nUsuario administrador creado:")
        print(f"  Correo:    {CORREO_ADMIN}")
        print(f"  Contraseña: {CONTRASENA_ADMIN}")
        print(f"\nYa puedes iniciar sesión en el frontend.")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
