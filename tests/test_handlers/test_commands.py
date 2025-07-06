"""Tests for command handlers."""

import pytest
from unittest.mock import AsyncMock, patch

from src.bot.handlers.commands import start, help_command, settings, stats


@pytest.mark.asyncio
async def test_start_command(mock_update, mock_context):
    """Test /start command."""
    mock_update.message.reply_text = AsyncMock()
    
    await start(mock_update, mock_context)
    
    mock_update.message.reply_text.assert_called_once()
    args, kwargs = mock_update.message.reply_text.call_args
    assert "Welcome" in args[0]
    assert kwargs["parse_mode"] == "HTML"


@pytest.mark.asyncio
async def test_help_command(mock_update, mock_context):
    """Test /help command."""
    mock_update.message.reply_text = AsyncMock()
    
    await help_command(mock_update, mock_context)
    
    mock_update.message.reply_text.assert_called_once()
    args, kwargs = mock_update.message.reply_text.call_args
    assert "Bot Commands" in args[0]
    assert kwargs["parse_mode"] == "HTML"


@pytest.mark.asyncio
async def test_settings_command(mock_update, mock_context):
    """Test /settings command."""
    mock_update.message.reply_text = AsyncMock()
    
    await settings(mock_update, mock_context)
    
    mock_update.message.reply_text.assert_called_once()
    args, kwargs = mock_update.message.reply_text.call_args
    assert "Bot Settings" in args[0]
    assert kwargs["parse_mode"] == "HTML"


@pytest.mark.asyncio
async def test_stats_command(mock_update, mock_context):
    """Test /stats command."""
    mock_update.message.reply_text = AsyncMock()
    
    await stats(mock_update, mock_context)
    
    mock_update.message.reply_text.assert_called_once()
    args, kwargs = mock_update.message.reply_text.call_args
    assert "Usage Statistics" in args[0]
    assert kwargs["parse_mode"] == "HTML"


@pytest.mark.asyncio
async def test_start_command_no_user(mock_update, mock_context):
    """Test /start command with no user."""
    mock_update.effective_user = None
    mock_update.message.reply_text = AsyncMock()
    
    await start(mock_update, mock_context)
    
    mock_update.message.reply_text.assert_not_called()


@pytest.mark.asyncio
async def test_help_command_no_user(mock_update, mock_context):
    """Test /help command with no user."""
    mock_update.effective_user = None
    mock_update.message.reply_text = AsyncMock()
    
    await help_command(mock_update, mock_context)
    
    mock_update.message.reply_text.assert_not_called()


@pytest.mark.asyncio
async def test_settings_command_no_user(mock_update, mock_context):
    """Test /settings command with no user."""
    mock_update.effective_user = None
    mock_update.message.reply_text = AsyncMock()
    
    await settings(mock_update, mock_context)
    
    mock_update.message.reply_text.assert_not_called()


@pytest.mark.asyncio
async def test_stats_command_no_user(mock_update, mock_context):
    """Test /stats command with no user."""
    mock_update.effective_user = None
    mock_update.message.reply_text = AsyncMock()
    
    await stats(mock_update, mock_context)
    
    mock_update.message.reply_text.assert_not_called()