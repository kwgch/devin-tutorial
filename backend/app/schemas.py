from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class FavoriteExpressionBase(BaseModel):
    japanese_text: str
    english_text: str
    note: Optional[str] = None

class FavoriteExpressionCreate(FavoriteExpressionBase):
    pass

class FavoriteExpression(FavoriteExpressionBase):
    id: str
    diary_entry_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class DiaryEntryBase(BaseModel):
    content: str

class DiaryEntryCreate(DiaryEntryBase):
    pass

class DiaryEntry(DiaryEntryBase):
    id: str
    translated_content: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    favorite_expressions: List[FavoriteExpression] = []

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
