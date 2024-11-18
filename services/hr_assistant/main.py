from fastapi import FastAPI, HTTPException
import gspread
from google.oauth2.service_account import Credentials
import os
from pydantic import BaseModel
from typing import Literal
import requests
from openai import OpenAI


# Define the scope for the API
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Initialize FastAPI app
app = FastAPI(root_path="/api")

# Path to your service account JSON key file
SERVICE_ACCOUNT_FILE = "client_secret.json"

# Google Sheet ID
SHEET_ID = "1fRpJK_MWDxvl8If39dNTR7nBYwyeanGlPRnr-ciIH14"

# Model configuration
OLLAMA_URL = "http://ollama_service:11434"
GEMMA_MODEL_NAME = "gemma2:2b"
OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPEN_AI_API_KEY environment variable is not set.")


class SkillRequest(BaseModel):
    prompt: str
    model: Literal["gemma2", "openai"]


class Gemma2LLM:
    def __init__(self, service_url: str, model_name: str):
        self.service_url = service_url
        self.model_name = model_name

    def ask_skill(self, prompt: str) -> str:
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

    def ask_skill(self, prompt: str) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that works in HR department."},
            {"role": "user", "content": f"{prompt}"},
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=500,
            temperature=0.7,
            n=1,
            stream=False,
        )
        return response.choices[0].message.content.strip()


gemma2_llm = Gemma2LLM(service_url=OLLAMA_URL, model_name=GEMMA_MODEL_NAME)
openai_llm = OpenAIChatLLM(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")


# API Endpoints
@app.post("/ask_skill_question/")
async def ask_skill_question(request: SkillRequest):
    try:
        matrix_data = _fetch_google_sheet_data()
        prompt = f"""
        You are an AI agent tasked to support Manager and HR to extract information form a competence matrix in Engineering Consultant Company. 

        The object contains dataset in JSON format.

        ### Matrix JSON data:
        {matrix_data}

        Respond to this question {request.prompt} using only the information provided in the matrix.

        - DO NOT use external sources or additional data.
        - DO NOT provide personal opinions or assumptions.
        - DO NOT include any information not present in the matrix.
        - Make you choice based on the information provided in the matrix.
        - Try to find patter in specific area of expertise(such as relate all data skills, all cloud skills, all programming skills, etc.)
        - Explain your answer, why you choose the candidate, and how you arrived at your conclusion.
        """

        if request.model == "gemma2":
            result = gemma2_llm.ask_skill(prompt)
        elif request.model == "openai":
            result = openai_llm.ask_skill(prompt)
        else:
            raise HTTPException(status_code=400, detail="Invalid model specified.")

        result = result.replace("\n", " ")

        return {"status": "success", "response": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _fetch_google_sheet_data():
    try:
        # Authenticate using the service account
        credentials = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )

        # Connect to Google Sheets
        gc = gspread.authorize(credentials)

        # Open the Google Sheet by its ID
        spreadsheet = gc.open_by_url(f"https://docs.google.com/spreadsheets/d/{SHEET_ID}")

        # Select the first worksheet
        worksheet = spreadsheet.worksheet("Sheet1")

        # Fetch all data as a list of dictionaries
        data = worksheet.get_all_records()

        return data

    except Exception as e:
        print(f"Error details: {str(e)}")
        raise Exception(f"Error fetching data from Google Sheets: {e}")
