from fastapi import APIRouter, HTTPException, Path, Body, Depends
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.diary import DiaryEntry as DiaryEntryModel, FavoriteExpression as FavoriteExpressionModel
from app.schemas import DiaryEntry, DiaryEntryCreate, FavoriteExpression
from app.db_config import get_db
from app.db_service import DatabaseService
from app.translation import translator
from app.auth import get_current_user, User

router = APIRouter()


@router.post("/diary", response_model=DiaryEntry)
async def create_diary_entry(
    entry: DiaryEntryCreate = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new diary entry with automatic translation."""
    db_service = DatabaseService(db)
    translated_content = translator.translate_japanese_to_english(entry.content)
    return db_service.create_diary_entry(current_user.id, entry.content, translated_content)


@router.get("/diary", response_model=List[DiaryEntry])
async def get_all_diary_entries(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all diary entries for the current user."""
    db_service = DatabaseService(db)
    return db_service.get_user_diary_entries(current_user.id)


@router.get("/diary/{entry_id}", response_model=DiaryEntry)
async def get_diary_entry(
    entry_id: str = Path(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific diary entry by ID."""
    db_service = DatabaseService(db)
    entry = db_service.get_diary_entry(entry_id)
    
    if not entry:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    
    if entry.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this diary entry")
    
    return entry


@router.put("/diary/{entry_id}", response_model=DiaryEntry)
async def update_diary_entry(
    entry_id: str = Path(...),
    entry: DiaryEntryCreate = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a diary entry with automatic translation."""
    db_service = DatabaseService(db)
    
    existing_entry = db_service.get_diary_entry(entry_id)
    if not existing_entry:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    
    if existing_entry.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this diary entry")
    
    translated_content = translator.translate_japanese_to_english(entry.content)
    updated_entry = db_service.update_diary_entry(entry_id, entry.content, translated_content)
    
    return updated_entry


@router.delete("/diary/{entry_id}")
async def delete_diary_entry(
    entry_id: str = Path(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a diary entry."""
    db_service = DatabaseService(db)
    
    existing_entry = db_service.get_diary_entry(entry_id)
    if not existing_entry:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    
    if existing_entry.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this diary entry")
    
    success = db_service.delete_diary_entry(entry_id)
    
    return {"message": "Diary entry deleted successfully"}


@router.post("/diary/{entry_id}/favorite", response_model=FavoriteExpression)
async def add_favorite_expression(
    entry_id: str = Path(...),
    japanese_text: str = Body(...),
    english_text: str = Body(...),
    note: Optional[str] = Body(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a favorite expression from a diary entry."""
    db_service = DatabaseService(db)
    
    existing_entry = db_service.get_diary_entry(entry_id)
    if not existing_entry:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    
    if existing_entry.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add favorite expressions to this diary entry")
    
    expression = db_service.add_favorite_expression(entry_id, japanese_text, english_text, note)
    
    return expression


@router.get("/favorites", response_model=List[FavoriteExpression])
async def get_all_favorite_expressions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all favorite expressions for the current user."""
    db_service = DatabaseService(db)
    return db_service.get_user_favorite_expressions(current_user.id)
