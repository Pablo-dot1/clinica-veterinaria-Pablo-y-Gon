# fastapi/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Crea una base para los modelos
Base = declarative_base()

# Configura la URL de la base de datos
DATABASE_URL = "sqlite:///./test.db"  # Usando SQLite como ejemplo, puedes cambiarla a la base de datos que estés usando

# Crea el motor de base de datos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # Para SQLite se necesita este argumento

# Crea una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea las tablas en la base de datos (si no existen)
def create_db():
    Base.metadata.create_all(bind=engine)
