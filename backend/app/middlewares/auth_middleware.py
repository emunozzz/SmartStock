from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decodificar_access_token
from app.repositories.usuario_repository import UsuarioRepository
from app.models.usuario_model import Usuario

oauth2_scheme = HTTPBearer()


def obtener_usuario_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    token = credenciales.credentials
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decodificar_access_token(token)
    if payload is None:
        raise credenciales_invalidas

    usuario_id = payload.get("sub")
    if usuario_id is None:
        raise credenciales_invalidas

    repository = UsuarioRepository(db)
    usuario = repository.obtener_por_id(int(usuario_id))
    if usuario is None or not usuario.activo:
        raise credenciales_invalidas

    return usuario