from sqlalchemy import Column, Integer, String, Boolean
from .session import Base

class NoteModel(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    is_persistent = Column(Boolean, default=True)
    bg_color = Column(String, default="#fef3c7")  # default bg color
    formatting = Column(String, nullable=True)   # JSON string with bold ranges