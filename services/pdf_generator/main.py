from fastapi import FastAPI, HTTPException
from fpdf import FPDF
import pandas as pd

app = FastAPI(
    root_path="/api"
)


@app.get("/generate_pdf/")
async def generate_pdf():
    try:
        # Example code for generating a PDF from a sample DataFrame
        df = pd.DataFrame({"Name": ["Alice", "Bob"], "Score": [85, 90]})
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add content to the PDF
        pdf.cell(200, 10, txt="Report", ln=True, align="C")
        for _, row in df.iterrows():
            pdf.cell(200, 10, txt=f"{row['Name']}: {row['Score']}", ln=True)

        # Save PDF
        # pdf.output("/data/report.pdf")
        result = "PDF generated successfully"

        return {"status": "success", "message": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
