"""Helper functions for the bot."""

import asyncio
import html
import re
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timezone

import aiohttp
from telegram import Update, User
from telegram.constants import ParseMode


def escape_markdown(text: str) -> str:
    """Escape special characters for Markdown."""
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return html.escape(text)


def get_user_mention(user: User, parse_mode: str = ParseMode.HTML) -> str:
    """Get user mention string."""
    if parse_mode == ParseMode.HTML:
        return f'<a href="tg://user?id={user.id}">{escape_html(user.first_name)}</a>'
    elif parse_mode == ParseMode.MARKDOWN_V2:
        return f'[{escape_markdown(user.first_name)}](tg://user?id={user.id})'
    else:
        return user.first_name


def get_user_info(user: User) -> Dict[str, Any]:
    """Extract user information."""
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'language_code': user.language_code,
        'is_bot': user.is_bot,
        'is_premium': user.is_premium,
    }


def format_timestamp(timestamp: datetime) -> str:
    """Format timestamp for display."""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")


def get_utc_now() -> datetime:
    """Get current UTC timestamp."""
    return datetime.now(timezone.utc)


def is_valid_url(url: str) -> bool:
    """Check if URL is valid."""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(url_pattern.match(url))


def split_message(text: str, max_length: int = 4096) -> List[str]:
    """Split long message into chunks."""
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    for line in text.split('\n'):
        if len(current_chunk) + len(line) + 1 <= max_length:
            current_chunk += line + '\n'
        else:
            if current_chunk:
                chunks.append(current_chunk.rstrip())
                current_chunk = line + '\n'
            else:
                # Line is too long, split it
                while len(line) > max_length:
                    chunks.append(line[:max_length])
                    line = line[max_length:]
                current_chunk = line + '\n'
    
    if current_chunk:
        chunks.append(current_chunk.rstrip())
    
    return chunks


async def download_file(url: str, timeout: int = 30) -> Optional[bytes]:
    """Download file from URL."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    return await response.read()
    except Exception:
        return None
    return None


async def rate_limit(calls_per_second: float = 1.0) -> None:
    """Simple rate limiting."""
    await asyncio.sleep(1.0 / calls_per_second)


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    # Remove or replace unsafe characters
    unsafe_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:255-len(ext)-1] + '.' + ext if ext else name[:255]
    
    return filename


def is_admin(user_id: int, admin_ids: List[int]) -> bool:
    """Check if user is admin."""
    return user_id in admin_ids


def get_command_args(text: str) -> List[str]:
    """Extract command arguments from message text."""
    parts = text.split()
    return parts[1:] if len(parts) > 1 else []


def format_error_message(error: Exception) -> str:
    """Format error message for user display."""
    error_messages = {
        'TimeoutError': 'Request timed out. Please try again.',
        'ConnectionError': 'Connection error. Please check your internet connection.',
        'ValueError': 'Invalid input. Please check your data.',
        'FileNotFoundError': 'File not found.',
        'PermissionError': 'Permission denied.',
    }
    
    error_type = type(error).__name__
    return error_messages.get(error_type, 'An unexpected error occurred. Please try again.')


def create_keyboard_chunks(items: List[str], chunk_size: int = 2) -> List[List[str]]:
    """Create keyboard button chunks."""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]