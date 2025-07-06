"""Pytest configuration and fixtures."""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from typing import Generator, AsyncGenerator

from telegram import Update, User, Message, Chat
from telegram.ext import ContextTypes

from src.bot.config import get_settings


@pytest.fixture
def settings():
    """Get test settings."""
    return get_settings()


@pytest.fixture
def mock_user():
    """Create a mock Telegram user."""
    return User(
        id=123456789,
        is_bot=False,
        first_name="Test",
        last_name="User",
        username="testuser",
        language_code="en",
        is_premium=False,
    )


@pytest.fixture
def mock_chat():
    """Create a mock Telegram chat."""
    return Chat(
        id=-123456789,
        type=Chat.PRIVATE,
        title="Test Chat",
        username="testchat",
    )


@pytest.fixture
def mock_message(mock_user, mock_chat):
    """Create a mock Telegram message."""
    return Message(
        message_id=1,
        date=None,
        chat=mock_chat,
        from_user=mock_user,
        text="Test message",
    )


@pytest.fixture
def mock_update(mock_message):
    """Create a mock Telegram update."""
    return Update(
        update_id=1,
        message=mock_message,
    )


@pytest.fixture
def mock_context():
    """Create a mock context."""
    context = Mock(spec=ContextTypes.DEFAULT_TYPE)
    context.bot = AsyncMock()
    context.user_data = {}
    context.chat_data = {}
    context.bot_data = {}
    context.args = []
    context.error = None
    return context


@pytest.fixture
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def mock_db_session():
    """Create a mock database session."""
    session = Mock()
    session.execute = AsyncMock()
    session.add = Mock()
    session.commit = Mock()
    session.rollback = Mock()
    session.refresh = Mock()
    session.delete = Mock()
    return session


@pytest.fixture
def mock_bot():
    """Create a mock bot."""
    bot = AsyncMock()
    bot.get_me = AsyncMock()
    bot.send_message = AsyncMock()
    bot.edit_message_text = AsyncMock()
    bot.delete_message = AsyncMock()
    return bot


class AsyncContextManager:
    """Helper class for async context managers."""
    
    def __init__(self, async_func):
        self.async_func = async_func
    
    async def __aenter__(self):
        return await self.async_func()
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.fixture
def async_context_manager():
    """Create an async context manager fixture."""
    return AsyncContextManager