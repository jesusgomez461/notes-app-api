from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship


# DOC: Note model for the database
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(50), nullable=False)
    content = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    version = Column(Integer, nullable=False, default=1)

    # DOC: Relations
    owner = relationship("User", back_populates="notes")
    category = relationship("Category", back_populates="notes")
    history = relationship(
        "NoteHistory", back_populates="note", cascade="all, delete"
    )
