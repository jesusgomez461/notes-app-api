from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship


# DOC: user model for the database
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    document = Column(String(12), nullable=False, unique=True, index=True)
    full_name = Column(String(70), nullable=False)
    email = Column(String(70), nullable=False, unique=True, index=True)
    password = Column(String(200), nullable=False)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)

    # DOC: Relationship with the notes table
    notes = relationship("Note", back_populates="owner")
