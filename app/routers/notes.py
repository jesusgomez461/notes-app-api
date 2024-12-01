from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.services.notes import (
    get_notes,
    create_note,
    get_note_by_id,
    update_note,
    delete_note,
)
from app.schemes.notes import NoteCreate, NoteUpdate, NoteResponse
from app.models import User
from app.core.security import get_current_user

router = APIRouter()


@router.get("/", response_model=List[NoteResponse])
async def read_notes(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Recuperar todas las notas del usuario autenticado.
    """
    notes = await get_notes(db, user_id=user.id)
    return notes


@router.get("/{note_id}", response_model=NoteResponse)
async def read_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Recuperar una nota específica del usuario autenticado.
    """
    note = await get_note_by_id(db, note_id=note_id, user_id=user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.post("/", response_model=NoteResponse)
async def create_new_note(
    note: NoteCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Crear una nueva nota para el usuario autenticado.
    """
    return await create_note(db, note, user_id=user.id)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_existing_note(
    note_id: int,
    note_update: NoteUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Actualizar una nota existente del usuario autenticado.
    """
    note = await update_note(
        db, note_id=note_id, note_update=note_update, user_id=user.id
    )
    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found or not authorized"
        )
    return note


@router.delete("/{note_id}", response_model=NoteResponse)
async def delete_existing_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Eliminar una nota existente del usuario autenticado.
    """
    note = await delete_note(db, note_id=note_id, user_id=user.id)
    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found or not authorized"
        )
    return note
