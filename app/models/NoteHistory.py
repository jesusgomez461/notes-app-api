from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship


# DOC: Note model for the database
class NoteHistory(Base):
    __tablename__ = "notes_history"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(50), nullable=False)
    content = Column(String(200), nullable=False)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    version = Column(Integer, nullable=False, default=1)
    note_id = Column(Integer, ForeignKey("notes.id"), nullable=False)

    # DOC: Relations
    note = relationship("Note", back_populates="history")
    category = relationship("Category", back_populates="notes_history")
