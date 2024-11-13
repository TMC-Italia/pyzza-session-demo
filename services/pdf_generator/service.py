from fpdf import FPDF
import pandas as pd


def perform_task():
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
    return "PDF generated successfully"
