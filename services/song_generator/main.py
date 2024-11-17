from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from service import generate_song_with_gemma
from service import pull_model



class SongRequest(BaseModel):
    prompt: str


app = FastAPI(
    root_path="/api"
)


@app.post("/generate_song/")
async def generate_song(request: SongRequest):
    try:
        result = generate_song_with_gemma(request.prompt)
        return {"status": "success", "song": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pull_model/")
async def pull():
    try:
        result = pull_model()
        return {"status": "success", "model": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
