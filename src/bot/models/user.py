"""User database model."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger, Text
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    """User model for storing Telegram user information."""
    
    __tablename__ = "users"
    
    # Telegram user information
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=True)
    username = Column(String(32), nullable=True, index=True)
    language_code = Column(String(10), nullable=True)
    
    # User status
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    is_premium = Column(Boolean, default=False, nullable=False)
    is_blocked = Column(Boolean, default=False, nullable=False)
    
    # Activity tracking
    last_activity = Column(DateTime, default=datetime.utcnow, nullable=False)
    message_count = Column(Integer, default=0, nullable=False)
    command_count = Column(Integer, default=0, nullable=False)
    
    # User preferences
    preferred_language = Column(String(10), default="en", nullable=False)
    timezone = Column(String(50), default="UTC", nullable=False)
    notifications_enabled = Column(Boolean, default=True, nullable=False)
    
    # Additional data
    bio = Column(Text, nullable=True)
    profile_photo_url = Column(String(500), nullable=True)
    
    def __repr__(self) -> str:
        """String representation of user."""
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
    
    @property
    def display_name(self) -> str:
        """Get user's display name (username or full name)."""
        return f"@{self.username}" if self.username else self.full_name
    
    def update_activity(self, message_type: str = "message") -> None:
        """Update user activity."""
        self.last_activity = datetime.utcnow()
        
        if message_type == "message":
            self.message_count += 1
        elif message_type == "command":
            self.command_count += 1
    
    def is_recently_active(self, days: int = 7) -> bool:
        """Check if user was active recently."""
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return self.last_activity > cutoff_date