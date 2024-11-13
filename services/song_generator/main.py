from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from service import perform_task


class SongRequest(BaseModel):
    prompt: str


app = FastAPI()


@app.post("/generate-song/")
async def generate_song(request: SongRequest):
    try:
        result = perform_task(request.prompt)
        return {"status": "success", "song": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
