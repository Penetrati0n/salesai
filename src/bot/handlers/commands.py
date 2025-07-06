"""Command handlers for the bot."""

from typing import Dict, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext

from ..utils.logging import get_logger, log_user_action, log_error
from ..utils.helpers import get_user_info, get_user_mention, format_error_message
from ..config import get_settings

logger = get_logger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    if not user:
        return
    
    log_user_action(logger, user.id, "start_command")
    
    welcome_message = (
        f"👋 Welcome {get_user_mention(user)}!\n\n"
        f"I'm a modern Telegram bot built with Python. "
        f"Here's what I can do:\n\n"
        f"🔧 Commands:\n"
        f"• /help - Show this help message\n"
        f"• /settings - Configure bot settings\n"
        f"• /stats - View usage statistics\n\n"
        f"📝 I can also process your messages, photos, and documents!\n\n"
        f"Use /help to see all available commands."
    )
    
    keyboard = [
        [InlineKeyboardButton("📚 Help", callback_data="help")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="settings")],
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
        parse_mode="HTML",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    user = update.effective_user
    if not user:
        return
    
    log_user_action(logger, user.id, "help_command")
    
    help_text = (
        "🤖 <b>Bot Commands</b>\n\n"
        "📋 <b>General Commands:</b>\n"
        "• /start - Start the bot and see welcome message\n"
        "• /help - Show this help message\n"
        "• /settings - Configure your preferences\n"
        "• /stats - View your usage statistics\n\n"
        "💬 <b>Message Processing:</b>\n"
        "• Send text messages for processing\n"
        "• Send photos for analysis\n"
        "• Send documents for processing\n"
        "• Send voice messages for transcription\n\n"
        "🔧 <b>Tips:</b>\n"
        "• Use inline keyboards for quick actions\n"
        "• Check your settings regularly\n"
        "• Report bugs or suggestions to the developer\n\n"
        "Need more help? Contact the developer!"
    )
    
    await update.message.reply_text(help_text, parse_mode="HTML")


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /settings command."""
    user = update.effective_user
    if not user:
        return
    
    log_user_action(logger, user.id, "settings_command")
    
    settings_text = (
        "⚙️ <b>Bot Settings</b>\n\n"
        "🔧 <b>Current Settings:</b>\n"
        "• Language: English\n"
        "• Notifications: Enabled\n"
        "• Privacy Mode: Standard\n"
        "• Response Format: HTML\n\n"
        "Use the buttons below to modify your settings."
    )
    
    keyboard = [
        [InlineKeyboardButton("🌐 Language", callback_data="setting_language")],
        [InlineKeyboardButton("🔔 Notifications", callback_data="setting_notifications")],
        [InlineKeyboardButton("🔒 Privacy", callback_data="setting_privacy")],
        [InlineKeyboardButton("📝 Format", callback_data="setting_format")],
        [InlineKeyboardButton("🔄 Reset", callback_data="setting_reset")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        settings_text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stats command."""
    user = update.effective_user
    if not user:
        return
    
    log_user_action(logger, user.id, "stats_command")
    
    # TODO: Implement actual statistics from database
    stats_text = (
        "📊 <b>Usage Statistics</b>\n\n"
        f"👤 <b>User:</b> {get_user_mention(user)}\n"
        f"🆔 <b>ID:</b> <code>{user.id}</code>\n\n"
        f"📈 <b>Activity:</b>\n"
        f"• Messages sent: 0\n"
        f"• Commands used: 0\n"
        f"• Files processed: 0\n"
        f"• Last activity: First time!\n\n"
        f"🏆 <b>Achievements:</b>\n"
        f"• New User 🎉\n\n"
        f"Keep using the bot to unlock more achievements!"
    )
    
    await update.message.reply_text(stats_text, parse_mode="HTML")


async def error_handler(update: Update, context: CallbackContext) -> None:
    """Handle errors that occur during message processing."""
    error = context.error
    user = update.effective_user if update else None
    
    if user:
        log_error(logger, error, {"user_id": user.id, "update": str(update)})
    else:
        log_error(logger, error, {"update": str(update)})
    
    # Send error message to user if possible
    if update and update.effective_message:
        error_message = format_error_message(error)
        try:
            await update.effective_message.reply_text(
                f"❌ {error_message}",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error("Failed to send error message", error=str(e))