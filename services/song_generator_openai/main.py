from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from service import generate_christmas_song



class SongRequest(BaseModel):
    prompt: str


app = FastAPI(
    root_path="/api"
)


@app.post("/generate_song/")
async def generate_song(request: SongRequest):
    try:
        result = generate_christmas_song(request.prompt)
        return {"status": "success", "song": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))