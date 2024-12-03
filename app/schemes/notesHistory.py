from pydantic import BaseModel
from datetime import datetime
from app.schemes.categories import CategoryResponse


class NoteHistoryCreate(BaseModel):
    title: str
    content: str
    version: int
    note_id: int


class NoteHistoryResponse(BaseModel):
    id: int
    title: str
    content: str
    created: datetime
    version: int
    note_id: int
    category: CategoryResponse

    class Config:
        orm_mode = True
