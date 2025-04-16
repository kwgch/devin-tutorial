import uuid
from datetime import datetime
from typing import Dict, List, Optional

from app.models import DiaryEntry, FavoriteExpression


class InMemoryDatabase:
    """In-memory database for diary entries."""
    
    def __init__(self):
        self.diary_entries: Dict[str, DiaryEntry] = {}
        self.favorite_expressions: List[FavoriteExpression] = []
    
    def create_diary_entry(self, content: str, translated_content: str) -> DiaryEntry:
        """Create a new diary entry."""
        entry_id = str(uuid.uuid4())
        now = datetime.now()
        
        entry = DiaryEntry(
            id=entry_id,
            content=content,
            translated_content=translated_content,
            created_at=now,
            updated_at=None,
            favorite_expressions=[]
        )
        
        self.diary_entries[entry_id] = entry
        return entry
    
    def get_diary_entry(self, entry_id: str) -> Optional[DiaryEntry]:
        """Get a diary entry by ID."""
        return self.diary_entries.get(entry_id)
    
    def get_all_diary_entries(self) -> List[DiaryEntry]:
        """Get all diary entries."""
        return list(self.diary_entries.values())
    
    def update_diary_entry(self, entry_id: str, content: str, translated_content: str) -> Optional[DiaryEntry]:
        """Update a diary entry."""
        if entry_id not in self.diary_entries:
            return None
        
        entry = self.diary_entries[entry_id]
        entry.content = content
        entry.translated_content = translated_content
        entry.updated_at = datetime.now()
        
        return entry
    
    def delete_diary_entry(self, entry_id: str) -> bool:
        """Delete a diary entry."""
        if entry_id not in self.diary_entries:
            return False
        
        del self.diary_entries[entry_id]
        return True
    
    def add_favorite_expression(self, entry_id: str, japanese_text: str, english_text: str, note: Optional[str] = None) -> Optional[FavoriteExpression]:
        """Add a favorite expression to a diary entry."""
        if entry_id not in self.diary_entries:
            return None
        
        expression = FavoriteExpression(
            japanese_text=japanese_text,
            english_text=english_text,
            note=note
        )
        
        entry = self.diary_entries[entry_id]
        entry.favorite_expressions.append(expression)
        self.favorite_expressions.append(expression)
        
        return expression
    
    def get_all_favorite_expressions(self) -> List[FavoriteExpression]:
        """Get all favorite expressions."""
        return self.favorite_expressions


db = InMemoryDatabase()
