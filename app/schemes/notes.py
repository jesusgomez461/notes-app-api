from pydantic import BaseModel
from datetime import datetime
from typing import List
from app.schemes.categories import CategoryResponse
from app.schemes.notesHistory import NoteHistoryResponse


class NoteCreate(BaseModel):
    title: str
    content: str
    category_id: int


class NoteUpdate(BaseModel):
    title: str
    content: str
    category_id: int
    # DOC: New field for optimistic concurrency control
    version: int


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created: datetime
    version: int
    history: List[NoteHistoryResponse]
    category: CategoryResponse

    class Config:
        orm_mode = True
