import asyncio
import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot import config
from bot.handlers import ollama

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message when the /start command is issued."""
    await update.message.reply_text("Hello! I'm your Telegram bot.")


def main():
    """Starts the bot."""
    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ollama.ask))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
