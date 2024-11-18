from sqlalchemy import create_engine, event, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
import os
import logging
from contextlib import contextmanager
from typing import Generator
import sqlite3

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/sql_app.db")

# Asegurar que el directorio de la base de datos existe
db_dir = os.path.dirname(SQLALCHEMY_DATABASE_URL.replace("sqlite:///", ""))
os.makedirs(db_dir, exist_ok=True)

# Configuración de SQLite para mejor rendimiento
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.execute("PRAGMA cache_size=10000")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

try:
    # Crear el motor de la base de datos con configuración optimizada
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={
            "check_same_thread": False,
            "timeout": 30
        },
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=True  # Esto ayudará a ver las consultas SQL en los logs
    )

    # Crear la sesión con configuración optimizada
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False
    )

    # Crear la base declarativa
    Base = declarative_base()

except Exception as e:
    logger.error(f"Error al configurar la base de datos: {str(e)}")
    raise

def init_db():
    """Inicializar la base de datos"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {str(e)}")
        raise

def check_database_connection():
    """Verificar la conexión a la base de datos"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.close()
        logger.info("Database connection check successful")
        return True
    except Exception as e:
        logger.error(f"Error al verificar la conexión a la base de datos: {str(e)}")
        raise

@contextmanager
def get_db_session() -> Generator:
    """Context manager para manejar sesiones de base de datos"""
    session = SessionLocal()
    try:
        logger.debug("Creating new database session")
        yield session
    except Exception as e:
        session.rollback()
        logger.error(f"Error en la sesión de base de datos: {str(e)}")
        raise
    finally:
        try:
            session.commit()
            logger.debug("Session committed successfully")
        except Exception as e:
            session.rollback()
            logger.error(f"Error al hacer commit de la sesión: {str(e)}")
            raise
        finally:
            session.close()
            logger.debug("Closing database session")

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
