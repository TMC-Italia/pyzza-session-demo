import os
from fastapi.middleware.cors import CORSMiddleware
from random import choice
from fastapi import FastAPI, HTTPException
import requests

# FROM ENV THE ALLOW
API_PORT = os.getenv("API_PORT", 3000)
API_PATH = f"http://localhost:{API_PORT}"

# Base URLs for other services, accessed by Docker Compose service names
PDF_GENERATOR_URL = "http://pdf_generator_service:8001/generate-pdf"
SONG_GENERATOR_URL = "http://song_generator_service:8002/generate-song"


app = FastAPI(
    title="PyZza session API",
    description="A simple Fast API to expose some python docker microservices.",
    version="0.1",
    docs_url="/docs",
    root_path="/api"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[API_PATH],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/trick-or-treat/")
async def trick_or_treat():
    """
    Get a random "trick" or "treat" response.
    """
    responses = {
        "treats": ["🍬 A virtual candy!", "🍫 A chocolate treat!"],
        "tricks": ["👻 A spooky story!", "🎃 A pumpkin surprise!"]
    }
    return choice(responses["treats"] + responses["tricks"])


@app.post("/generate_pdf/")
async def generate_pdf():
    try:
        response = requests.post(PDF_GENERATOR_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {e}")


@app.post("/generate_song/")
async def generate_song(prompt: str):
    try:
        # Send a prompt for song generation
        response = requests.post(SONG_GENERATOR_URL, json={"prompt": prompt})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error generating song: {e}")
