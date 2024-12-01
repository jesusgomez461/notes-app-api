from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("Error: No se cargó la URL de la base de datos desde el archivo "
          ".env")
DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Crear el motor asincrónico
engine = create_async_engine(DATABASE_URL, echo=True)

# Crear la sesión asincrónica
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base para los modelos
Base = declarative_base()


# Dependencia para obtener la sesión de base de datos
async def get_db():
    async with async_session() as session:
        yield session
