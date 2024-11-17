from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Crea una base para los modelos
Base = declarative_base()

# Configura la URL de la base de datos
DATABASE_URL = "sqlite:///./test.db"  # Usando SQLite como ejemplo

# Crea el motor de base de datos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crea una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crea las tablas en la base de datos
def create_db():
    import db_models  # Importar los modelos aquí para evitar importación circular
    Base.metadata.create_all(bind=engine)
