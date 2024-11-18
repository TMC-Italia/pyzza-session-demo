import os
from fastapi.middleware.cors import CORSMiddleware
from random import choice
from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
from typing import Literal


# FROM ENV THE ALLOW
API_PORT = os.getenv("API_PORT", 8000)
API_PATH = f"http://localhost:{API_PORT}"

# Base URLs for other services, accessed by Docker Compose service names
HR_ASSISTANT_URL = "http://hr_assistant_service:8001/api"
SONG_GENERATOR_URL = "http://song_generator_service:8002/api"

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


class SongRequest(BaseModel):
    prompt: str
    model: Literal["gemma2", "openai"]  # Define allowed model values


@app.get("/example/trick-or-treat/")
async def trick_or_treat():
    """
    Get a random "trick" or "treat" response.
    """
    responses = {
        "treats": [
            "🍬 A virtual candy!", 
            "🍫 A chocolate treat!", 
            "A crepy crawly spider!",
            "A ghostly apparition!",
            "A spooky skeleton!",
        ],
        "tricks": [
            "👻 A spooky story!", 
            "🎃 A pumpkin surprise!",
            "A scary monster!",
            "A haunted house!",
            "A witch's spell!",
        ],
    }
    return choice(responses["treats"] + responses["tricks"])


@app.get("/bc_data/generate_pdf/")
async def generate_pdf():
    try:
        response = requests.get(HR_ASSISTANT_URL + "/generate_pdf")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {e}")


@app.post("/bc_data/ask_question/")
async def ask_question(request: SongRequest):
    try:
        to_json = request.model_dump()
        response = requests.post(HR_ASSISTANT_URL + "/ask_skill_question", json=to_json)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error generating responding your questions: {e}")


@app.post("/song_generator/generate_song/")
async def generate_song(song_request: SongRequest):
    try:
        to_json = song_request.model_dump()
        response = requests.post(SONG_GENERATOR_URL + "/generate_song", json=to_json)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error generating song: {e}")


@app.get("/song_generator/pull_model/")
async def pull_model():
    try:
        response = requests.get(SONG_GENERATOR_URL + "/pull_model")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error generating song: {e}")