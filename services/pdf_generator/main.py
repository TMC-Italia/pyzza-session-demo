from fastapi import FastAPI, HTTPException
from fpdf import FPDF
import gspread
from google.oauth2.service_account import Credentials
import io

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


@app.get("/generate_pdf/")
async def generate_pdf():
    try:
        # Fetch data from Google Sheets
        data = fetch_google_sheet_data()

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def fetch_google_sheet_data():
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


def create_pdf(data):
    try:
        # Initialize PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add a title
        pdf.cell(200, 10, txt="Report", ln=True, align="C")

        # Add table headers
        if data:
            headers = data[0].keys()
            for header in headers:
                pdf.cell(40, 10, txt=header, border=1)
            pdf.ln()

            # Add table rows
            for row in data:
                for header in headers:
                    pdf.cell(40, 10, txt=str(row[header]), border=1)
                pdf.ln()
        else:
            pdf.cell(200, 10, txt="No data available.", ln=True)

        # Save PDF to a bytes buffer
        pdf_output = io.BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)

        # return pdf_output

        return "ok"

    except Exception as e:
        raise Exception(f"Error generating PDF: {e}")
