from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
import os
import requests
from openai import OpenAI

# Initialize FastAPI application
app = FastAPI(
    root_path="/api"
)


# Model configuration
OLLAMA_URL = "http://ollama_service:11434"
GEMMA_MODEL_NAME = "gemma2:2b"
OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPEN_AI_API_KEY environment variable is not set.")


class SongRequest(BaseModel):
    prompt: str
    model: Literal["gemma2", "openai"]  # Define allowed model values


class Gemma2LLM:
    def __init__(self, service_url: str, model_name: str):
        self.service_url = service_url
        self.model_name = model_name

    def generate_song(self, prompt: str) -> str:
        payload = {"model": self.model_name, "prompt": prompt, "stream": False}
        response = requests.post(f"{self.service_url}/api/generate", json=payload)
        if response.status_code == 200:
            try:
                response_json = response.json()
                return response_json.get("response", "No response from model")
            except ValueError:
                raise ValueError("Invalid JSON response from Gemma2 service.")
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Gemma2 service error: {response.text}"
            )


class OpenAIChatLLM:
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_song(self, prompt: str) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that composes Christmas songs."},
            {"role": "user", "content": f"{prompt}"},
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=150,
            temperature=0.7,
            n=1,
            stream=False,
        )
        return response.choices[0].message.content.strip()


gemma2_llm = Gemma2LLM(service_url=OLLAMA_URL, model_name=GEMMA_MODEL_NAME)
openai_llm = OpenAIChatLLM(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")


# API Endpoints
@app.post("/generate_song/")
async def generate_song(request: SongRequest):
    try:
        prompt = (
            f"Generate a Christmas song that includes the following words: {request.prompt}.\n"
            "The song should be at least 100 words long and no more than 300 words long.\n"
            "It should be in the style of a Christmas carol, about Christmas, Santa Claus, or other Christmas-related topics.\n"
            "The song should be cheerful and festive, and should include rhyming verses."
        )

        if request.model == "gemma2":
            result = gemma2_llm.generate_song(prompt)
        elif request.model == "openai":
            result = openai_llm.generate_song(prompt)
        else:
            raise HTTPException(status_code=400, detail="Invalid model specified.")

        return {"status": "success", "song": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pull_model/")
def pull_model():
    response = requests.post(
        url="http://ollama_service:11434/api/pull",
        json={"model": "gemma2:2b"}
    )

    if response.status_code == 200:
        print("Model pulled successfully.")
        return True
    print(f"Failed to pull model: {response.status_code} - {response.text}")
    return False
