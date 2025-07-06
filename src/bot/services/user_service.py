"""User service for managing user operations."""

from typing import Optional, List, Dict, Any
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from telegram import User as TelegramUser

from ..models.user import User
from ..utils.logging import get_logger

logger = get_logger(__name__)


class UserService:
    """Service for managing user operations."""
    
    def __init__(self, db_session: Session):
        """Initialize user service."""
        self.db = db_session
    
    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Get user by Telegram ID."""
        try:
            stmt = select(User).where(User.telegram_id == telegram_id)
            result = self.db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Error getting user by telegram_id", error=str(e), telegram_id=telegram_id)
            return None
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        try:
            stmt = select(User).where(User.username == username)
            result = self.db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Error getting user by username", error=str(e), username=username)
            return None
    
    async def create_user(self, telegram_user: TelegramUser) -> Optional[User]:
        """Create a new user from Telegram user data."""
        try:
            user = User(
                telegram_id=telegram_user.id,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name,
                username=telegram_user.username,
                language_code=telegram_user.language_code,
                is_premium=telegram_user.is_premium or False,
                preferred_language=telegram_user.language_code or "en",
            )
            
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            
            logger.info("User created", user_id=user.id, telegram_id=user.telegram_id)
            return user
        
        except Exception as e:
            logger.error("Error creating user", error=str(e), telegram_id=telegram_user.id)
            self.db.rollback()
            return None
    
    async def update_user(self, user: User, **kwargs) -> Optional[User]:
        """Update user information."""
        try:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            user.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(user)
            
            logger.info("User updated", user_id=user.id, telegram_id=user.telegram_id)
            return user
        
        except Exception as e:
            logger.error("Error updating user", error=str(e), user_id=user.id)
            self.db.rollback()
            return None
    
    async def get_or_create_user(self, telegram_user: TelegramUser) -> Optional[User]:
        """Get existing user or create new one."""
        user = await self.get_user_by_telegram_id(telegram_user.id)
        
        if user:
            # Update user information if it has changed
            updated_data = {}
            if user.first_name != telegram_user.first_name:
                updated_data["first_name"] = telegram_user.first_name
            if user.last_name != telegram_user.last_name:
                updated_data["last_name"] = telegram_user.last_name
            if user.username != telegram_user.username:
                updated_data["username"] = telegram_user.username
            if user.language_code != telegram_user.language_code:
                updated_data["language_code"] = telegram_user.language_code
            
            if updated_data:
                user = await self.update_user(user, **updated_data)
        else:
            user = await self.create_user(telegram_user)
        
        return user
    
    async def update_user_activity(self, user: User, activity_type: str = "message") -> None:
        """Update user activity."""
        try:
            user.update_activity(activity_type)
            self.db.commit()
        except Exception as e:
            logger.error("Error updating user activity", error=str(e), user_id=user.id)
            self.db.rollback()
    
    async def get_active_users(self, days: int = 30) -> List[User]:
        """Get active users within specified days."""
        try:
            from datetime import timedelta
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            stmt = select(User).where(
                User.last_activity > cutoff_date,
                User.is_active == True
            )
            result = self.db.execute(stmt)
            return result.scalars().all()
        
        except Exception as e:
            logger.error("Error getting active users", error=str(e))
            return []
    
    async def get_user_stats(self, user: User) -> Dict[str, Any]:
        """Get user statistics."""
        return {
            "user_id": user.id,
            "telegram_id": user.telegram_id,
            "username": user.username,
            "full_name": user.full_name,
            "joined_date": user.created_at.isoformat(),
            "last_activity": user.last_activity.isoformat(),
            "message_count": user.message_count,
            "command_count": user.command_count,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
            "is_premium": user.is_premium,
            "days_since_join": (datetime.utcnow() - user.created_at).days,
            "days_since_last_activity": (datetime.utcnow() - user.last_activity).days,
        }
    
    async def block_user(self, user: User) -> Optional[User]:
        """Block a user."""
        return await self.update_user(user, is_blocked=True, is_active=False)
    
    async def unblock_user(self, user: User) -> Optional[User]:
        """Unblock a user."""
        return await self.update_user(user, is_blocked=False, is_active=True)
    
    async def make_admin(self, user: User) -> Optional[User]:
        """Make user an admin."""
        return await self.update_user(user, is_admin=True)
    
    async def remove_admin(self, user: User) -> Optional[User]:
        """Remove admin privileges from user."""
        return await self.update_user(user, is_admin=False)
    
    async def delete_user(self, user: User) -> bool:
        """Delete a user."""
        try:
            self.db.delete(user)
            self.db.commit()
            logger.info("User deleted", user_id=user.id, telegram_id=user.telegram_id)
            return True
        except Exception as e:
            logger.error("Error deleting user", error=str(e), user_id=user.id)
            self.db.rollback()
            return False