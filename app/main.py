from fastapi import FastAPI
from app.db.database import engine
from app.models import (
    Base
)
from app.routers import auth, notes  # Importa tus routers
import uvicorn

# Instancia de la aplicación FastAPI
app = FastAPI(
    title="Notes App",
    description="API para gestionar usuarios y notas",
    version="1.0.0",
)


# Evento de inicio para crear las tablas
@app.on_event("startup")
async def startup():
    # Crear las tablas si no existen
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Evento de apagado para cerrar el motor de la base de datos
@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()

# Registrar los routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(notes.router, prefix="/api/notes", tags=["Notes"])


# Ruta raíz (opcional)
@app.get("/")
async def root():
    return {"message": "Welcome to the Notes App API"}

# Inicia el servidor si se ejecuta directamente
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
