from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime, timezone

class Base (SQLModel):
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    deleted_at: datetime | None = Field(default=None)