from sqlmodel import SQLModel, Field, DateTime, Column
from datetime import datetime, timedelta
from app.core.settings import settings
from uuid import uuid4, UUID

class ShortUrl(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    original_url: str = Field(max_length=2048)
    short_code: str = Field(index=True, unique=True)
    created_at: datetime = Field(sa_column=Column(DateTime, nullable=False), default_factory=lambda: settings.time_now())
    expires_at: datetime = Field(sa_column=Column(DateTime, nullable=False), default_factory=lambda: settings.time_now() + timedelta(hours=(settings.short_url_ttl_seconds / 3600)))
    access_count: int = Field(default=0)