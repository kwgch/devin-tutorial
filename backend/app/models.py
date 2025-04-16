from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class DiaryEntryBase(BaseModel):
    """Base model for diary entries."""
    content: str = Field(..., description="The Japanese content of the diary entry")


class DiaryEntryCreate(DiaryEntryBase):
    """Model for creating a diary entry."""
    pass


class FavoriteExpression(BaseModel):
    """Model for favorite expressions."""
    japanese_text: str = Field(..., description="The Japanese text of the expression")
    english_text: str = Field(..., description="The English translation of the expression")
    note: Optional[str] = Field(None, description="Optional note about the expression")


class DiaryEntry(DiaryEntryBase):
    """Model for a diary entry with translation."""
    id: str = Field(..., description="Unique identifier for the diary entry")
    translated_content: str = Field(..., description="The English translation of the diary entry")
    created_at: datetime = Field(..., description="When the entry was created")
    updated_at: Optional[datetime] = Field(None, description="When the entry was last updated")
    favorite_expressions: List[FavoriteExpression] = Field(default=[], description="Favorite expressions from this entry")
