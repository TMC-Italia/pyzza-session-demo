from fastapi import FastAPI
from kafka_producer import send_task
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="PyZza session API",
    description="A simple API to show python microservices.",
    version="0.1",
    docs_url="/docs",
    root_path="/"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate_pdf/")
async def generate_pdf():
    task_data = {"type": "pdf", "content": "Sample data for PDF"}
    send_task("pdf_task", task_data)
    return {"status": "success", "message": "PDF generation task submitted"}

@app.post("/generate_chart/")
async def generate_chart():
    task_data = {"type": "chart", "content": "Sample data for Chart"}
    send_task("chart_task", task_data)
    return {"status": "success", "message": "Chart generation task submitted"}

@app.post("/generate_song/")
async def generate_song(prompt: str):
    task_data = {"type": "song", "prompt": prompt}
    send_task("song_task", task_data)
    return {"status": "success", "message": "Song generation task submitted"}
