from fastapi import FastAPI, HTTPException
from service import perform_task

app = FastAPI(
    root_path="/api"
)


@app.post("/generate-pdf/")
async def generate_pdf():
    try:
        result = perform_task()
        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
