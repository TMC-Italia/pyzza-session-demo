FROM python:3.9-slim

# Install dependencies
WORKDIR /app/bot
COPY bot.py app/bot/bot.py
RUN pip install python-telegram-bot requests

# Get env from compose
ARG TELEGRAM_BOT_TOKEN

#Run the bot
CMD ["python", "bot.py"]
