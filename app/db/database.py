from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("Error: Failed to load database URL from .env file")
DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# DOC: Create the asynchronous motor
engine = create_async_engine(DATABASE_URL, echo=True)

# DOC: Create asynchronous session
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# DOC: Basis for models
Base = declarative_base()


# DOC: Dependency to obtain database session
async def get_db():
    async with async_session() as session:
        yield session
