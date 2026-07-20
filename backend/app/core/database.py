from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings


# Motor de conexión a PostgreSQL.
# pool_pre_ping evita errores por conexiones "muertas" que PostgreSQL
# cierra tras un tiempo de inactividad (muy común en entornos de desarrollo).
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

# Fábrica de sesiones: cada petición HTTP tendrá su propia sesión,
# nunca se comparte una sesión entre peticiones distintas.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Clase base de la que heredarán todos los modelos SQLAlchemy (tablas).
Base = declarative_base()


def get_db():
    """
    Dependencia de FastAPI. Entrega una sesión de base de datos
    a cada endpoint que la solicite, y garantiza que se cierre
    correctamente incluso si ocurre un error durante la petición.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()