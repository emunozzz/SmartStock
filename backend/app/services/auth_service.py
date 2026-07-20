from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.usuario_repository import UsuarioRepository
from app.core.security import verificar_contrasena, crear_access_token
from app.schemas.auth_schema import LoginRequest, TokenResponse


class AuthService:

    def __init__(self, db: Session):
        self.repository = UsuarioRepository(db)

    def login(self, datos: LoginRequest) -> TokenResponse:
        usuario = self.repository.obtener_por_correo(datos.correo)

        credenciales_invalidas = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

        if not usuario:
            raise credenciales_invalidas
        if not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo, contacte al administrador"
            )
        if not verificar_contrasena(datos.contrasena, usuario.contrasena_hash):
            raise credenciales_invalidas

        token = crear_access_token(data={
            "sub": str(usuario.usuario_id),
            "rol_id": usuario.rol_id
        })
        return TokenResponse(access_token=token)