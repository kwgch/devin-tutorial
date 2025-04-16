from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import List, Optional
from sqlalchemy.ext.declarative import declarative_base

from app.db_config import Base
from app.models.base import generate_uuid

class DiaryEntry(Base):
    """Diary entry model."""
    __tablename__ = "diary_entries"

    id = Column(String, primary_key=True, default=generate_uuid)
    content = Column(Text, nullable=False)
    translated_content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    user = relationship("User", back_populates="diary_entries")
    favorite_expressions = relationship("FavoriteExpression", back_populates="diary_entry", cascade="all, delete-orphan")


class FavoriteExpression(Base):
    """Favorite expression model."""
    __tablename__ = "favorite_expressions"

    id = Column(String, primary_key=True, default=generate_uuid)
    japanese_text = Column(Text, nullable=False)
    english_text = Column(Text, nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    diary_entry_id = Column(String, ForeignKey("diary_entries.id"), nullable=False)
    
    diary_entry = relationship("DiaryEntry", back_populates="favorite_expressions")
