from fastapi import FastAPI, HTTPException
import gspread
from google.oauth2.service_account import Credentials
import os
from pydantic import BaseModel
from typing import Literal
import requests
from openai import OpenAI
import matplotlib.pyplot as plt
import pandas as pd
from fastapi.responses import FileResponse
import seaborn as sns


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

Chart_Type = Literal["histogram", "bar_chart", "scatter_plot"]
Skills = Literal["Python", "SQL", "Power BI", "Tableau", "R", "Java", "C++", "C#", "JavaScript", "AWS", "Azure", "GCP"]
OUTPUT_DIR = "charts"


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


if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


@app.get("/matrix_charts/{chart_type}/{skill}")
async def matrix_charts(chart_type: Chart_Type, skill: str = None):
    """
    API endpoint to fetch data, generate a specified chart, and return it as a file response.

    Args:
        chart_type (Chart_Type): The type of chart to generate (e.g., histogram, scatter_plot).
        skill (str): Comma-separated skill names for the chart. 
            For scatter_plot, exactly two skills must be provided.
        name (str): Name of the individual for radar chart.
        role (str): Role for radar chart.

    Returns:
        FileResponse: The generated chart as a file response.
    """
    try:
        # Fetch data from Google Sheets
        matrix_data = _fetch_complete_google_sheet_data()

        # Convert JSON data to Pandas DataFrame
        df = pd.DataFrame(matrix_data)

        # Create the specified chart
        file = _create_charts(df, chart_type, skill)

        # Return the generated chart as a response
        return FileResponse(file, media_type="image/png", filename=f"{chart_type}_{skill.replace(',', '_')}.png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating chart: {str(e)}")


def _fetch_complete_google_sheet_data():
    """
    Helper function to fetch data from Google Sheets and return it as JSON.
    """
    try:
        # Authenticate using the service account
        credentials = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        gc = gspread.authorize(credentials)

        # Open the Google Sheet by its ID
        spreadsheet = gc.open_by_url(f"https://docs.google.com/spreadsheets/d/{SHEET_ID}")

        # Select the worksheet "AllData"
        worksheet = spreadsheet.worksheet("AllData")

        # Fetch all data as a list of dictionaries
        data = worksheet.get_all_records()

        return data

    except Exception as e:
        print(f"Error details: {str(e)}")
        raise Exception(f"Error fetching data from Google Sheets: {e}")


def _create_charts(df: pd.DataFrame, chart_type: Chart_Type, skill: str = None) -> str:
    """
    Helper function to create different types of charts based on the specified chart_type.

    Args:
        df (pd.DataFrame): The data for the chart.
        chart_type (Chart_Type): The type of chart to create.
        skill (str): Comma-separated skill names for the chart.

    Returns:
        str: The file path to the generated chart.
    """
    try:
        if chart_type == "histogram":
            return _create_histogram(df, skill)
        elif chart_type == "bar_chart":
            return _create_bar_chart(df)
        elif chart_type == "scatter_plot":
            skills = skill.split(",")  # Split the comma-separated skills
            if len(skills) != 2:
                raise ValueError("Scatter plot requires exactly two skills (e.g., 'skill1,skill2').")
            return _create_scatter_plot(df, skills)
        else:
            raise ValueError(f"Invalid chart type: {chart_type}")
    except Exception as e:
        raise Exception(f"Error creating charts: {e}")


def _create_histogram(df: pd.DataFrame, skill: Skills) -> str:
    """Helper function to create a histogram of Power BI ratings."""
    plt.figure(figsize=(10, 6))

    # Ensure the column is numeric, coerce invalid values to NaN
    skill = skill or "Power BI"
    numeric_column = pd.to_numeric(df[skill], errors="coerce")

    # Drop rows with NaN values
    numeric_column = numeric_column.dropna()

    numeric_column.hist(bins=10, edgecolor='black')
    plt.title(f"Histogram of {skill} Ratings")
    plt.xlabel("Rating")
    plt.ylabel("Frequency")
    path = f"{OUTPUT_DIR}/histogram.png"
    plt.savefig(path)
    plt.close()
    return path


def _create_bar_chart(df: pd.DataFrame) -> str:
    """Helper function to create a bar chart of employee roles."""
    plt.figure(figsize=(12, 8))

    # Count valid roles
    role_counts = df["Role"].dropna().value_counts()

    role_counts.plot(kind="bar")
    plt.title("Number of Employees by Role")
    plt.xlabel("Role")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha='right')
    path = f"{OUTPUT_DIR}/employee_roles_bar_chart.png"
    plt.savefig(path)
    plt.close()
    return path


def _create_scatter_plot(df: pd.DataFrame, skills: list) -> str:
    """Helper function to create a scatter plot for two skills."""
    plt.figure(figsize=(10, 6))

    # Extract and clean data for the specified skills
    x = pd.to_numeric(df[skills[0]], errors="coerce")
    y = pd.to_numeric(df[skills[1]], errors="coerce")

    # Drop rows with NaN values in either column
    valid_data = pd.DataFrame({skills[0]: x, skills[1]: y}).dropna()

    sns.scatterplot(x=valid_data[skills[0]], y=valid_data[skills[1]], alpha=0.7)
    plt.title(f"Scatter Plot: {skills[0]} vs {skills[1]}")
    plt.xlabel(f"{skills[0]} Rating")
    plt.ylabel(f"{skills[1]} Rating")

    path = f"{OUTPUT_DIR}/scatter_{skills[0]}_vs_{skills[1]}.png"
    plt.savefig(path)
    plt.close()
    return path
