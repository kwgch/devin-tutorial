import uuid
from datetime import datetime
from typing import Dict, List, Optional

from app.models import DiaryEntry, FavoriteExpression
from app.auth import User, UserCreate


class InMemoryDatabase:
    """In-memory database for diary entries and users."""
    
    def __init__(self):
        self.diary_entries: Dict[str, DiaryEntry] = {}
        self.favorite_expressions: List[FavoriteExpression] = []
        self.users: Dict[str, User] = {}
        self.user_entries: Dict[str, List[str]] = {}  # Maps user_id to list of entry_ids
        self.user_passwords: Dict[str, str] = {}  # Maps user_id to hashed password
    
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
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        user_id = str(uuid.uuid4())
        now = datetime.now()
        
        user = User(
            id=user_id,
            email=user_data.email,
            name=user_data.name,
            picture=user_data.picture,
            created_at=now
        )
        
        self.users[user_id] = user
        self.user_entries[user_id] = []
        
        # Store hashed password
        from app.auth import get_password_hash
        self.user_passwords[user_id] = get_password_hash(user_data.password)
        
        return user
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        return self.users.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        for user in self.users.values():
            if user.email == email:
                return user
        return None
        
    def verify_user_password(self, email: str, password: str) -> Optional[User]:
        """Verify user credentials and return user if valid."""
        user = self.get_user_by_email(email)
        if user and user.id in self.user_passwords:
            from app.auth import verify_password
            if verify_password(password, self.user_passwords[user.id]):
                return user
        return None
        
def get_user_by_email(email: str) -> Optional[User]:
    """Get a user by email."""
    return db.get_user_by_email(email)


db = InMemoryDatabase()
