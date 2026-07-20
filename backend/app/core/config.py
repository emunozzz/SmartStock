from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración central de la aplicación SmartStock.
    Los valores se cargan automáticamente desde el archivo .env
    ubicado en la raíz de backend/.
    """

    # Información general de la aplicación
    APP_NAME: str = "SmartStock API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Base de datos
    DATABASE_URL: str

    # Seguridad / JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Groq
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


# Instancia única reutilizable en todo el proyecto
settings = Settings()