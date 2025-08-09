import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from bot.config import TELEGRAM_BOT_TOKEN
from bot.handlers import gemini_handler

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message when the /start command is issued."""
    await update.message.reply_text("Hello! I'm your Telegram bot.")


def main() -> None:
    """Starts the bot."""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", gemini_handler.ask))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, gemini_handler.mention)
    )

    logger.info("Bot started polling...")
    app.run_polling()


if __name__ == "__main__":
    main()
