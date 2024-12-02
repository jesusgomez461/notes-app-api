import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.main import app
from app.db.database import get_db
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


# Fixture para configurar el motor de base de datos de prueba
@pytest.fixture(scope="session")
async def test_engine():
    """
    Configura el motor de base de datos en memoria para pruebas.
    """
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Crea las tablas
    try:
        yield engine
    finally:
        await engine.dispose()  # Asegura que se cierre


# Fixture para manejar sesiones de base de datos en pruebas
@pytest.fixture(scope="function")
async def test_db_session(test_engine):
    """
    Proporciona una sesión de base de datos para cada prueba.
    Se asegura de hacer rollback al finalizar.
    """
    async_session = sessionmaker(
        bind=test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.rollback()


# Fixture para anular la dependencia de get_db
@pytest.fixture(scope="function", autouse=True)
def override_get_db(test_db_session):
    """
    Sobrescribe la dependencia de FastAPI para usar la base de datos de prueba.
    """
    async def _override_get_db():
        async with test_db_session as session:
            yield session
    app.dependency_overrides[get_db] = _override_get_db


# Fixture para crear un cliente asíncrono de pruebas
@pytest.fixture
async def async_client():
    """
    Crea un cliente asíncrono usando ASGITransport para pruebas.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        try:
            yield client
        finally:
            await client.aclose()  # Asegura que se cierre el cliente
