from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import os

# FastAPI Base URL
API_BASE_URL = "http://api_service:8000/api"


# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message."""
    await update.message.reply_text("Welcome! Use /trickortreat, /generatepdf, or /generatesong  /askskill or /pullmodel. commands.")


async def trick_or_treat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Call the trick-or-treat API."""
    try:
        response = requests.get(f"{API_BASE_URL}/example/trick-or-treat/")
        response.raise_for_status()
        result = response.text
        await update.message.reply_text(f"🎉 {result}")
    except requests.RequestException as e:
        await update.message.reply_text(f"Error: {e}")


async def generate_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Call the generate_song API with multiple prompts."""
    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage: /generatesong <model (gemma2 or openai)> <prompt1> [prompt2] [prompt3]..."
        )
        return

    model = context.args[0]
    prompts = " ".join(context.args[1:])

    if model not in ["gemma2", "openai"]:
        await update.message.reply_text("Invalid model. Use 'gemma2' or 'openai'.")
        return

    payload = {"prompt": prompts, "model": model}
    try:
        response = requests.post(f"{API_BASE_URL}/song_generator/generate_song/", json=payload)
        response.raise_for_status()
        result = response.json()
        await update.message.reply_text(f"Song Generated: {result}")
    except requests.RequestException as e:
        await update.message.reply_text(f"Error: {e}")


async def ask_skill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Call the generate_song API with multiple prompts."""
    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage: /askskill <model (gemma2 or openai)> <prompt1> [prompt2] [prompt3]..."
        )
        return

    model = context.args[0]
    prompts = " ".join(context.args[1:])

    if model not in ["gemma2", "openai"]:
        await update.message.reply_text("Invalid model. Use 'gemma2' or 'openai'.")
        return

    payload = {"prompt": prompts, "model": model}
    try:
        response = requests.post(f"{API_BASE_URL}/bc_data/ask_question/", json=payload)
        response.raise_for_status()
        result = response.json()
        await update.message.reply_text(f"Response: {result}")
    except requests.RequestException as e:
        await update.message.reply_text(f"Error: {e}")


async def generate_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Call the generate_pdf API."""
    try:
        response = requests.post(f"{API_BASE_URL}/bc_data/generate_pdf/")
        response.raise_for_status()
        result = response.json()
        await update.message.reply_text(f"PDF Generated: {result}")
    except requests.RequestException as e:
        await update.message.reply_text(f"Error: {e}")


async def pull_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Call the pull_model API."""
    try:
        response = requests.get(f"{API_BASE_URL}/song_generator/pull_model/")
        response.raise_for_status()
        result = response.json()
        await update.message.reply_text(f"Model pulled: {result}")
    except requests.RequestException as e:
        await update.message.reply_text(f"Error: {e}")


# Main Function
def main():
    # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram Bot token
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    # Create the Application
    app = Application.builder().token(TOKEN).build()

    # Add Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("trickortreat", trick_or_treat))
    app.add_handler(CommandHandler("generatepdf", generate_pdf))
    app.add_handler(CommandHandler("generatesong", generate_song))
    app.add_handler(CommandHandler("pullmodel", pull_model))
    app.add_handler(CommandHandler("askskill", ask_skill))

    # Run the bot
    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
