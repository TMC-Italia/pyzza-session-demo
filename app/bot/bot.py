import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# Get the Telegram token from the Docker environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
FASTAPI_URL = "http://localhost:8000/trick-or-treat/"  # points to FastAPI container


async def trick_or_treat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(FASTAPI_URL)
    message = response.json().get("message", "No trick or treat available.")
    await update.message.reply_text(message)


def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("trickortreat", trick_or_treat))
    application.run_polling()


if __name__ == "__main__":
    main()
