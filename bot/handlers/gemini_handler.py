"""Telegram bot handlers for querying Gemini API."""

import logging

from telegram import Update
from telegram.ext import CallbackContext

from bot.clients import gemini_client

logger = logging.getLogger(__name__)


async def ask(update: Update, context: CallbackContext) -> None:
    """
    Handles /ask command that queries Gemini API.
    Replied-to message is used as additional context.
    """
    if not context.args:
        await update.message.reply_text("Usage: /ask <your question>")
        return

    question = " ".join(context.args)
    # Use text from the replied message as context if available.
    reply_context = (
        update.message.reply_to_message.text
        if update.message.reply_to_message and update.message.reply_to_message.text
        else None
    )

    try:
        answer = gemini_client.ask(question, reply_context)
    except Exception as e:
        logger.error("Error processing /ask command: %s", e)
        answer = (
            "An error occurred while processing your request. Please try again later."
        )

    await update.message.reply_text(answer)


async def mention(update: Update, context: CallbackContext) -> None:
    """
    Handles messages that mention the bot or reply to bot's messages.
    Replied-to message is used as additional context.
    """
    bot_username = context.bot.username
    text = update.message.text or ""
    trigger = False
    reply_context = ""

    # Check if the message is a reply to a bot's message.
    if (
        update.message.reply_to_message
        and update.message.reply_to_message.from_user.is_bot
    ):
        trigger = True
        reply_context = update.message.reply_to_message.text or None

    # Check if the bot is mentioned in the message.
    if f"@{bot_username}" in text:
        trigger = True
        # Remove the mention from the text.
        text = text.replace(f"@{bot_username}", "").strip()

    if trigger and text:
        try:
            answer = gemini_client.ask(text, reply_context)
        except Exception as e:
            logger.error(f"Error processing mention: {e}")
            answer = "An error occurred while processing your request. Please try again later."
        await update.message.reply_text(answer)
