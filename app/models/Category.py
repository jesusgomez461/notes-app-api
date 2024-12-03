from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship


# DOC: category model for the database
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(20), nullable=False, index=True)
    color = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # DOC: Relationship with the users table
    user = relationship("User", back_populates="categories")
    notes = relationship("Note", back_populates="category")
    notes_history = relationship("NoteHistory", back_populates="category")
