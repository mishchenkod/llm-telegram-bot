"""Environment variables and configuration."""

from os import getenv

from dotenv import load_dotenv

load_dotenv(".env")

TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")
