from fastapi import APIRouter, HTTPException, Path, Body
from typing import List, Optional

from app.models import DiaryEntryCreate, DiaryEntry, FavoriteExpression
from app.database import db
from app.translation import translator

router = APIRouter()


@router.post("/diary", response_model=DiaryEntry)
async def create_diary_entry(entry: DiaryEntryCreate = Body(...)):
    """Create a new diary entry with automatic translation."""
    translated_content = translator.translate_japanese_to_english(entry.content)
    return db.create_diary_entry(entry.content, translated_content)


@router.get("/diary", response_model=List[DiaryEntry])
async def get_all_diary_entries():
    """Get all diary entries."""
    return db.get_all_diary_entries()


@router.get("/diary/{entry_id}", response_model=DiaryEntry)
async def get_diary_entry(entry_id: str = Path(...)):
    """Get a specific diary entry by ID."""
    entry = db.get_diary_entry(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    return entry


@router.put("/diary/{entry_id}", response_model=DiaryEntry)
async def update_diary_entry(
    entry_id: str = Path(...),
    entry: DiaryEntryCreate = Body(...)
):
    """Update a diary entry with automatic translation."""
    translated_content = translator.translate_japanese_to_english(entry.content)
    updated_entry = db.update_diary_entry(entry_id, entry.content, translated_content)
    
    if not updated_entry:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    
    return updated_entry


@router.delete("/diary/{entry_id}")
async def delete_diary_entry(entry_id: str = Path(...)):
    """Delete a diary entry."""
    success = db.delete_diary_entry(entry_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    
    return {"message": "Diary entry deleted successfully"}


@router.post("/diary/{entry_id}/favorite", response_model=FavoriteExpression)
async def add_favorite_expression(
    entry_id: str = Path(...),
    japanese_text: str = Body(...),
    english_text: str = Body(...),
    note: Optional[str] = Body(None)
):
    """Add a favorite expression from a diary entry."""
    expression = db.add_favorite_expression(entry_id, japanese_text, english_text, note)
    
    if not expression:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    
    return expression


@router.get("/favorites", response_model=List[FavoriteExpression])
async def get_all_favorite_expressions():
    """Get all favorite expressions."""
    return db.get_all_favorite_expressions()
