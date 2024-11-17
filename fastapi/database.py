from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

try:
    # Crear el motor de la base de datos
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},  # Solo necesario para SQLite
        pool_pre_ping=True  # Verificar conexión antes de usar
    )

    # Crear la sesión
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Crear la base declarativa
    Base = declarative_base()

except Exception as e:
    logger.error(f"Error al configurar la base de datos: {str(e)}")
    raise

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Error en la sesión de base de datos: {str(e)}")
        raise
    finally:
        db.close()
