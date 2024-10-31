from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os

# Set up environment variables
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://api_service:8000")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Initialize the bot application
app = Application.builder().token(TELEGRAM_TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /generate_pdf, /generate_chart, or /generate_song to create tasks.")


async def generate_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Call FastAPI endpoint to submit a PDF task
    response = requests.post(f"{FASTAPI_URL}/generate_pdf")
    if response.status_code == 200:
        task_id = response.json()["task_id"]
        await update.message.reply_text(f"PDF generation task submitted! Task ID: {task_id}")
    else:
        await update.message.reply_text("Failed to submit PDF task.")


async def generate_chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Call FastAPI endpoint to submit a Chart task
    response = requests.post(f"{FASTAPI_URL}/generate_chart")
    if response.status_code == 200:
        task_id = response.json()["task_id"]
        await update.message.reply_text(f"Chart generation task submitted! Task ID: {task_id}")
    else:
        await update.message.reply_text("Failed to submit Chart task.")


async def generate_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the prompt from the user
    if not context.args:
        await update.message.reply_text("Please provide a prompt after /generate_song command.")
        return
    prompt = " ".join(context.args)

    # Call FastAPI endpoint to submit a Song generation task
    response = requests.post(f"{FASTAPI_URL}/generate_song", json={"prompt": prompt})
    if response.status_code == 200:
        task_id = response.json()["task_id"]
        await update.message.reply_text(f"Song generation task submitted! Task ID: {task_id}")
    else:
        await update.message.reply_text("Failed to submit Song task.")


async def check_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the task_id from the user
    if not context.args:
        await update.message.reply_text("Please provide a task ID after /check_status command.")
        return
    task_id = context.args[0]

    # Call FastAPI endpoint to check task status
    response = requests.get(f"{FASTAPI_URL}/get_result/{task_id}")
    if response.status_code == 200:
        result = response.json()
        if result["status"] == "completed":
            await update.message.reply_text(f"Task completed! Result: {result['result']}")
        else:
            await update.message.reply_text("Task is still being processed.")
    else:
        await update.message.reply_text("Failed to retrieve task status.")

# Define bot command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("generate_pdf", generate_pdf))
app.add_handler(CommandHandler("generate_chart", generate_chart))
app.add_handler(CommandHandler("generate_song", generate_song))
app.add_handler(CommandHandler("check_status", check_status))

# Start the bot
if __name__ == "__main__":
    app.run_polling()
