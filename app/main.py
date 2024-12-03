from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import engine
from app.models import Base
from app.routers import auth, notes, categories, notesHistory
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # DOC: Start event: Create tables if it does not exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # DOC: Shutdown event: Shut down database engine
    await engine.dispose()

# DOC: FastAPI application instance with lifecycle handler
app = FastAPI(
    title="Notes App",
    description="API para agregar notas por usuario",
    version="1.0.0",
    lifespan=lifespan,
)

# DOC: Middleware to allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # DOC: Allow only this origin
    allow_credentials=True,
    allow_methods=["*"],  # DOC: Allow all methods
    allow_headers=["*"],  # DOC: Allow all headers
)

# DOC: Register routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(notes.router, prefix="/api/notes", tags=["Notes"])
app.include_router(
    categories.router,
    prefix="/api/categories",
    tags=["Categories"]
)
app.include_router(
    notesHistory.router,
    prefix="/api/notes-history",
    tags=["NotesHistory"]
)

# DOC: Starts the server
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
