from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import NoteHistory
from app.models import Note
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import joinedload, subqueryload


# DOC: Service to restore note from history
async def restore_note_from_history(db: AsyncSession, history_id: int):
    try:
        # DOC: Search for the entry in notes_history by its ID
        result = await db.execute(
            select(NoteHistory)
            .options(joinedload(NoteHistory.category))
            .where(NoteHistory.id == history_id)
        )
        note_history = result.scalar_one_or_none()

        if not note_history:
            raise HTTPException(
                status_code=404,
                detail="noteHistoryNotFound"
            )

        # DOC: Search for the note associated with the note history
        result = await db.execute(
            select(Note)
            .options(
                subqueryload(Note.history).joinedload(NoteHistory.category),
                joinedload(Note.category)
            )
            .where(Note.id == note_history.note_id)
        )
        note = result.scalar_one_or_none()

        if not note:
            raise HTTPException(
                status_code=404,
                detail="associatedNoteNotFound"
            )

        # DOC: Restore the note with the data from the note history
        note.title = note_history.title
        note.content = note_history.content
        note.category_id = note_history.category_id
        note.version = note_history.version

        # DOC: Delete the note history entry
        await db.delete(note_history)

        await db.commit()
        await db.refresh(note)
        return note

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="integrityError"
        )
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="databaseError"
        )
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="unknownError"
        )


# DOC: Service to delete note history with user authenticated and note_id
async def delete_note_history(
    db: AsyncSession, note_history_id: int
):
    try:
        result = await db.execute(
            select(NoteHistory)
            .options(joinedload(NoteHistory.category))
            .where(NoteHistory.id == note_history_id)
        )
        db_note_history = result.scalar_one_or_none()

        if not db_note_history:
            raise HTTPException(
                status_code=404,
                detail="noteHistoryNotFound"
            )

        await db.delete(db_note_history)
        await db.commit()
        return db_note_history

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="databaseError"
        )
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="internalServerError"
        )
