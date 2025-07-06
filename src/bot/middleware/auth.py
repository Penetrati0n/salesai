"""Authentication middleware for the bot."""

from typing import Optional, List
from telegram import Update
from telegram.ext import ContextTypes

from ..utils.logging import get_logger
from ..config import get_settings

logger = get_logger(__name__)


class AuthMiddleware:
    """Middleware for handling authentication and authorization."""
    
    def __init__(self, admin_ids: Optional[List[int]] = None):
        """Initialize auth middleware."""
        self.admin_ids = admin_ids or []
        self.settings = get_settings()
    
    async def check_user_access(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Check if user has access to the bot."""
        user = update.effective_user
        
        if not user:
            logger.warning("No user found in update")
            return False
        
        # Check if user is blocked (this would be implemented with database)
        if await self.is_user_blocked(user.id):
            logger.warning("Blocked user attempted access", user_id=user.id)
            return False
        
        # Log user access
        logger.info("User access granted", user_id=user.id, username=user.username)
        return True
    
    async def check_admin_access(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Check if user has admin access."""
        user = update.effective_user
        
        if not user:
            return False
        
        # Check if user is admin
        if user.id in self.admin_ids:
            logger.info("Admin access granted", user_id=user.id, username=user.username)
            return True
        
        # Check if user is admin in database (this would be implemented with database)
        if await self.is_user_admin(user.id):
            logger.info("Admin access granted (from database)", user_id=user.id, username=user.username)
            return True
        
        logger.warning("Admin access denied", user_id=user.id, username=user.username)
        return False
    
    async def is_user_blocked(self, user_id: int) -> bool:
        """Check if user is blocked."""
        # TODO: Implement database check
        return False
    
    async def is_user_admin(self, user_id: int) -> bool:
        """Check if user is admin in database."""
        # TODO: Implement database check
        return False
    
    async def rate_limit_check(self, user_id: int) -> bool:
        """Check if user is rate limited."""
        # TODO: Implement rate limiting logic
        return False
    
    async def log_user_activity(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Log user activity."""
        user = update.effective_user
        message = update.effective_message
        
        if not user:
            return
        
        activity_data = {
            "user_id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "chat_id": message.chat.id if message else None,
            "message_type": message.content_type if message else None,
        }
        
        logger.info("User activity logged", **activity_data)
    
    def require_admin(self, func):
        """Decorator to require admin access."""
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            if not await self.check_admin_access(update, context):
                await update.message.reply_text("❌ Admin access required.")
                return
            return await func(update, context, *args, **kwargs)
        return wrapper
    
    def require_auth(self, func):
        """Decorator to require user authentication."""
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            if not await self.check_user_access(update, context):
                await update.message.reply_text("❌ Access denied.")
                return
            await self.log_user_activity(update, context)
            return await func(update, context, *args, **kwargs)
        return wrapper