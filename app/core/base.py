from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime, timezone

class Base (SQLModel):
    
    id: Optional[int] = Field(default=None, primary_key=True)

    activo: bool = Field(default=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable = False)

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable = False)

    deleted_at: Optional[datetime] = Field(default=None, nullable = True)