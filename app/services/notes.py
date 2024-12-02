from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Note
from app.schemes.notes import NoteCreate, NoteUpdate
from datetime import datetime, timezone


# DOC: Service to get all notes from user
async def get_notes(db: AsyncSession, user_id: int):
    result = await db.execute(select(Note).where(Note.user_id == user_id))
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
        user_id=user_id,
        created=datetime.now(timezone.utc),
    )
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note


# DOC: Service to update note with user authenticated
async def update_note(
        db: AsyncSession,
        note_id: int,
        note_update: NoteUpdate,
        user_id: int):
    result = await db.execute(
        select(Note).where(Note.id == note_id, Note.user_id == user_id))
    db_note = result.scalar_one_or_none()
    if db_note:
        db_note.title = note_update.title
        db_note.content = note_update.content
        await db.commit()
        await db.refresh(db_note)
    return db_note


# DOC: Service to delete note with user authenticated
async def delete_note(db: AsyncSession, note_id: int, user_id: int):
    result = await db.execute(
        select(Note).where(Note.id == note_id, Note.user_id == user_id)
        )
    db_note = result.scalar_one_or_none()
    if db_note:
        await db.delete(db_note)
        await db.commit()
    return db_note
