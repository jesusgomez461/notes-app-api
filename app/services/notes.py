from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Note, NoteHistory
from app.schemes.notes import NoteCreate, NoteUpdate
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, subqueryload


# DOC: Service to get all notes from user
async def get_notes(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Note)
        .options(
            subqueryload(Note.history).joinedload(NoteHistory.category),
            joinedload(Note.category)
        )
        .where(Note.user_id == user_id)
    )
    return result.scalars().all()


# DOC: Service to get note by id
async def get_note_by_id(db: AsyncSession, note_id: int, user_id: int):
    result = await db.execute(
        select(Note).where(Note.id == note_id, Note.user_id == user_id)
    )
    return result.scalar_one_or_none()


# DOC: Service to create note with user authenticated
async def create_note(db: AsyncSession, note: NoteCreate, user_id: int):
    db_note = Note(
        title=note.title,
        content=note.content,
        category_id=note.category_id,
        user_id=user_id,
        created=datetime.now(),
    )
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    result = await db.execute(
        select(Note)
        .options(
            subqueryload(Note.history),
            joinedload(Note.category)
        )
        .where(Note.id == db_note.id)
    )
    db_note = result.scalar_one_or_none()
    return db_note


# DOC: Service to update note with user authenticated
async def update_note(
        db: AsyncSession,
        note_id: int,
        note_update: NoteUpdate,
        user_id: int):
    # DOC: Obtain the note corresponding to the authenticated user
    result = await db.execute(
        select(Note)
        .options(
            subqueryload(Note.history).subqueryload(NoteHistory.category),
            joinedload(Note.category)
        )
        .where(Note.id == note_id, Note.user_id == user_id)
    )
    db_note = result.scalar_one_or_none()

    if not db_note:
        raise HTTPException(status_code=404, detail="noteDoesNotExist")

    if note_update.version != db_note.version:
        raise HTTPException(
            status_code=409,
            detail="updateError"
        )

    # DOC: Create a new note history
    note_history = NoteHistory(
        note_id=db_note.id,
        title=db_note.title,
        content=db_note.content,
        version=db_note.version,
        category_id=db_note.category_id,
        created=datetime.now()
    )
    db.add(note_history)

    # DOC: Performing the update
    db_note.title = note_update.title
    db_note.content = note_update.content
    db_note.category_id = note_update.category_id
    db_note.version += 1

    try:
        await db.commit()
        await db.refresh(db_note, ["history", "category"])
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="updateErrorNote")

    return db_note


# DOC: Service to delete note with user authenticated
async def delete_note(db: AsyncSession, note_id: int, user_id: int):
    result = await db.execute(
        select(Note)
        .options(
            subqueryload(Note.history),
            joinedload(Note.category)
        )
        .where(Note.id == note_id, Note.user_id == user_id)
    )
    db_note = result.scalar_one_or_none()

    if db_note:
        await db.delete(db_note)
        await db.commit()

    return db_note
