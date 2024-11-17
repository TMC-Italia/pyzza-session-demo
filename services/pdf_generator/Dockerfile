# Dockerfile

FROM python:3.9-slim

# Copy the entire project to the container
COPY . /pdf_generator

# Copy the application code
COPY main.py /pdf_generator/main.py
COPY service.py /pdf_generator/service.py
COPY requirements.txt /pdf_generator/requirements.txt

WORKDIR /pdf_generator

# Install dependencies
RUN pip install -r requirements.txt

# Expose the service on a specific port
EXPOSE 8001

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
