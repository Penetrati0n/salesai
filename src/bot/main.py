"""Main bot entry point."""

import asyncio
import signal
import sys
from typing import NoReturn

from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from .config import get_settings
from .handlers import commands, messages
from .utils.logging import configure_logging, get_logger

# Configure logging
configure_logging()
logger = get_logger(__name__)


async def setup_bot() -> Application:
    """Set up the bot application."""
    settings = get_settings()
    
    # Create application
    application = Application.builder().token(settings.bot_token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", commands.start))
    application.add_handler(CommandHandler("help", commands.help_command))
    application.add_handler(CommandHandler("settings", commands.settings))
    application.add_handler(CommandHandler("stats", commands.stats))
    
    # Add message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages.handle_text))
    application.add_handler(MessageHandler(filters.PHOTO, messages.handle_photo))
    application.add_handler(MessageHandler(filters.DOCUMENT, messages.handle_document))
    application.add_handler(MessageHandler(filters.VOICE, messages.handle_voice))
    
    # Add error handler
    application.add_error_handler(commands.error_handler)
    
    logger.info("Bot application configured successfully")
    return application


async def main() -> NoReturn:
    """Main bot function."""
    settings = get_settings()
    logger.info("Starting bot", version="0.1.0", environment=settings.environment)
    
    try:
        # Set up the bot
        application = await setup_bot()
        
        # Set up signal handlers for graceful shutdown
        def signal_handler(signum, frame):
            logger.info("Received signal, shutting down gracefully", signal=signum)
            asyncio.create_task(application.stop())
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start the bot
        if settings.webhook_url:
            # Use webhook
            await application.run_webhook(
                listen="0.0.0.0",
                port=settings.webhook_port,
                url_path=settings.webhook_path,
                key=None,
                cert=None,
                webhook_url=settings.webhook_url + settings.webhook_path,
            )
        else:
            # Use polling
            await application.run_polling(
                allowed_updates=["message", "callback_query", "inline_query"],
                drop_pending_updates=True,
            )
    
    except Exception as e:
        logger.error("Fatal error occurred", error=str(e), exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error("Failed to start bot", error=str(e), exc_info=True)
        sys.exit(1)