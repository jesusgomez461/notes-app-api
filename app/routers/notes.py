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


@router.get(
    "/",
    response_model=List[NoteResponse],
    summary="Read Notes",
    description="Read all notes from authenticate user"
)
async def read_notes(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Read all notes from authenticate user
    """
    notes = await get_notes(db, user_id=user.id)
    return notes


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
    summary="Read Note",
    description="Read a specific note from authenticate user"
)
async def read_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Read a specific note from authenticate user
    - **note_id**: ID of the note
    """
    note = await get_note_by_id(db, note_id=note_id, user_id=user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.post(
    "/",
    response_model=NoteResponse,
    summary="Create Note",
    description="Create a new note from authenticate user"
)
async def create_new_note(
    note: NoteCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Create a new note from authenticate user
    - **title**: Title of the note
    - **content**: Content of the note
    """
    return await create_note(db, note, user_id=user.id)


@router.put(
    "/{note_id}",
    response_model=NoteResponse,
    summary="Update Note",
    description="Update a specific note from authenticate user"
)
async def update_existing_note(
    note_id: int,
    note_update: NoteUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Update a specific note from authenticate user
    - **note_id**: ID of the note
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


@router.delete(
    "/{note_id}",
    response_model=NoteResponse,
    summary="Delete Note",
    description="Delete a specific note from authenticate user"
)
async def delete_existing_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Delete a specific note from authenticate user
    - **note_id**: ID of the note
    """
    note = await delete_note(db, note_id=note_id, user_id=user.id)
    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found or not authorized"
        )
    return note
