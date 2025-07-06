"""Message handlers for the bot."""

from typing import Optional
from telegram import Update, Message
from telegram.ext import ContextTypes

from ..utils.logging import get_logger, log_user_action
from ..utils.helpers import get_user_info, split_message, sanitize_filename
from ..config import get_settings

logger = get_logger(__name__)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages."""
    user = update.effective_user
    message = update.effective_message
    
    if not user or not message or not message.text:
        return
    
    log_user_action(logger, user.id, "text_message", text_length=len(message.text))
    
    # Process the text message
    text = message.text.strip()
    
    # Echo the message back with some processing
    response = (
        f"📝 <b>Message Received!</b>\n\n"
        f"👤 <b>From:</b> {user.first_name}\n"
        f"📊 <b>Length:</b> {len(text)} characters\n"
        f"🔤 <b>Words:</b> {len(text.split())}\n\n"
        f"<b>Your message:</b>\n<blockquote>{text}</blockquote>\n\n"
        f"<i>This is an echo bot. In a real implementation, "
        f"you would process this message according to your bot's logic.</i>"
    )
    
    # Split long messages if necessary
    messages = split_message(response)
    
    for msg in messages:
        await message.reply_text(msg, parse_mode="HTML")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle photo messages."""
    user = update.effective_user
    message = update.effective_message
    
    if not user or not message or not message.photo:
        return
    
    log_user_action(logger, user.id, "photo_message")
    
    # Get the largest photo
    photo = message.photo[-1]
    
    response = (
        f"📷 <b>Photo Received!</b>\n\n"
        f"👤 <b>From:</b> {user.first_name}\n"
        f"🆔 <b>File ID:</b> <code>{photo.file_id}</code>\n"
        f"📏 <b>Size:</b> {photo.width}x{photo.height} pixels\n"
        f"💾 <b>File Size:</b> {photo.file_size} bytes\n\n"
        f"<i>Photo processing would be implemented here.</i>"
    )
    
    if message.caption:
        response += f"\n\n<b>Caption:</b>\n<blockquote>{message.caption}</blockquote>"
    
    await message.reply_text(response, parse_mode="HTML")


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle document messages."""
    user = update.effective_user
    message = update.effective_message
    
    if not user or not message or not message.document:
        return
    
    log_user_action(logger, user.id, "document_message")
    
    document = message.document
    
    response = (
        f"📄 <b>Document Received!</b>\n\n"
        f"👤 <b>From:</b> {user.first_name}\n"
        f"📝 <b>Name:</b> {document.file_name or 'Unknown'}\n"
        f"🗂️ <b>MIME Type:</b> {document.mime_type or 'Unknown'}\n"
        f"💾 <b>Size:</b> {document.file_size} bytes\n"
        f"🆔 <b>File ID:</b> <code>{document.file_id}</code>\n\n"
        f"<i>Document processing would be implemented here.</i>"
    )
    
    if message.caption:
        response += f"\n\n<b>Caption:</b>\n<blockquote>{message.caption}</blockquote>"
    
    # Check file type and provide specific responses
    if document.mime_type:
        if document.mime_type.startswith('image/'):
            response += "\n\n🖼️ <i>This appears to be an image file.</i>"
        elif document.mime_type.startswith('video/'):
            response += "\n\n🎥 <i>This appears to be a video file.</i>"
        elif document.mime_type.startswith('audio/'):
            response += "\n\n🎵 <i>This appears to be an audio file.</i>"
        elif document.mime_type in ['application/pdf']:
            response += "\n\n📋 <i>This appears to be a PDF document.</i>"
        elif document.mime_type in ['text/plain', 'text/csv']:
            response += "\n\n📄 <i>This appears to be a text file.</i>"
    
    await message.reply_text(response, parse_mode="HTML")


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle voice messages."""
    user = update.effective_user
    message = update.effective_message
    
    if not user or not message or not message.voice:
        return
    
    log_user_action(logger, user.id, "voice_message")
    
    voice = message.voice
    
    response = (
        f"🎤 <b>Voice Message Received!</b>\n\n"
        f"👤 <b>From:</b> {user.first_name}\n"
        f"⏱️ <b>Duration:</b> {voice.duration} seconds\n"
        f"💾 <b>Size:</b> {voice.file_size} bytes\n"
        f"🆔 <b>File ID:</b> <code>{voice.file_id}</code>\n\n"
        f"<i>Voice message transcription would be implemented here.</i>"
    )
    
    await message.reply_text(response, parse_mode="HTML")


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle video messages."""
    user = update.effective_user
    message = update.effective_message
    
    if not user or not message or not message.video:
        return
    
    log_user_action(logger, user.id, "video_message")
    
    video = message.video
    
    response = (
        f"🎥 <b>Video Received!</b>\n\n"
        f"👤 <b>From:</b> {user.first_name}\n"
        f"⏱️ <b>Duration:</b> {video.duration} seconds\n"
        f"📏 <b>Size:</b> {video.width}x{video.height} pixels\n"
        f"💾 <b>File Size:</b> {video.file_size} bytes\n"
        f"🆔 <b>File ID:</b> <code>{video.file_id}</code>\n\n"
        f"<i>Video processing would be implemented here.</i>"
    )
    
    if message.caption:
        response += f"\n\n<b>Caption:</b>\n<blockquote>{message.caption}</blockquote>"
    
    await message.reply_text(response, parse_mode="HTML")


async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle audio messages."""
    user = update.effective_user
    message = update.effective_message
    
    if not user or not message or not message.audio:
        return
    
    log_user_action(logger, user.id, "audio_message")
    
    audio = message.audio
    
    response = (
        f"🎵 <b>Audio Received!</b>\n\n"
        f"👤 <b>From:</b> {user.first_name}\n"
        f"🎼 <b>Title:</b> {audio.title or 'Unknown'}\n"
        f"🎤 <b>Artist:</b> {audio.performer or 'Unknown'}\n"
        f"⏱️ <b>Duration:</b> {audio.duration} seconds\n"
        f"💾 <b>Size:</b> {audio.file_size} bytes\n"
        f"🆔 <b>File ID:</b> <code>{audio.file_id}</code>\n\n"
        f"<i>Audio processing would be implemented here.</i>"
    )
    
    if message.caption:
        response += f"\n\n<b>Caption:</b>\n<blockquote>{message.caption}</blockquote>"
    
    await message.reply_text(response, parse_mode="HTML")


async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle sticker messages."""
    user = update.effective_user
    message = update.effective_message
    
    if not user or not message or not message.sticker:
        return
    
    log_user_action(logger, user.id, "sticker_message")
    
    sticker = message.sticker
    
    response = (
        f"🎭 <b>Sticker Received!</b>\n\n"
        f"👤 <b>From:</b> {user.first_name}\n"
        f"😀 <b>Emoji:</b> {sticker.emoji or 'None'}\n"
        f"📦 <b>Set Name:</b> {sticker.set_name or 'Unknown'}\n"
        f"📏 <b>Size:</b> {sticker.width}x{sticker.height} pixels\n"
        f"🆔 <b>File ID:</b> <code>{sticker.file_id}</code>\n\n"
        f"<i>Nice sticker! 👍</i>"
    )
    
    await message.reply_text(response, parse_mode="HTML")