from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de datos para MySQL
# Reemplaza 'usuario', 'contraseña', y 'nombre_de_la_base_de_datos' con tus credenciales y la base de datos que estés usando
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://Pablo:contraseña@localhost/nombre_de_la_base_de_datos"



# Crear el motor de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear la clase para la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la clase base para los modelos
Base = declarative_base()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()  # Abre una sesión a la base de datos
    try:
        yield db  # Devuelve la sesión
    finally:
        db.close()  # Cierra la sesión una vez que haya terminado la operación
