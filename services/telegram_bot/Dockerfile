# Use an official Python image
FROM python:3.10-slim


# Copy the entire project to the container
COPY . /bot
WORKDIR /bot

# Install dependencies
RUN pip install -r requirements.txt


# Command to run the bot
CMD ["python", "main.py"]
