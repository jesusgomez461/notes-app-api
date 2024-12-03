from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.notesHistory import (
    restore_note_from_history,
    delete_note_history,
)
from app.schemes.notesHistory import NoteHistoryResponse
from app.schemes.notes import NoteResponse
from app.models import User
from app.core.security import get_current_user

router = APIRouter()


@router.put(
    "/restore/{history_id}",
    response_model=NoteResponse,
    summary="Restore Note",
    description="Restore a note from a specific notes_history entry"
)
async def restore_note(
    history_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Restore a note from a specific notes_history entry.
    """
    if not user:
        raise HTTPException(
            status_code=404,
            detail="userNotFound"
        )
    note = await restore_note_from_history(db, history_id)
    return note


@router.delete(
    "/{note_history_id}",
    response_model=NoteHistoryResponse,
    summary="Delete Note History",
    description="Delete a specific note history from authenticate user"
)
async def delete_existing_note_history(
    note_history_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Delete a specific note from authenticate user
    - **note_history_id**: ID of the note
    """
    note_history = await delete_note_history(
        db, note_history_id=note_history_id,
    )
    if not note_history:
        raise HTTPException(
            status_code=404,
            detail="noteDoesNotExist"
        )
    return note_history
