import os
from fastapi import FastAPI
from random import choice
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

app = FastAPI(
    title="Trick or Treat API",
    description="A simple API to get a trick or treat message.",
    version="0.1",
    docs_url="/docs",
    root_path="/api"
)


@app.get("/trick-or-treat/", tags=["trick-or-treat"], response_description="Get a trick or treat message.")
async def trick_or_treat():
    responses = {
        "treats": ["🍬 A virtual candy!", "🍫 A chocolate treat!"],
        "tricks": ["👻 A spooky story!", "🎃 A pumpkin surprise!"]
    }
    return {"message": choice(responses["treats"] + responses["tricks"])}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))  # Use PORT environment variable or default to 3000
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=True)



@app.post("/generate-pdf/")
async def generate_pdf(file: UploadFile = File(...)):
    # Load the uploaded Excel file into a DataFrame
    contents = await file.read()
    df = pd.read_excel(contents)

    # Define Macro Categories for skills
    categories = {
        "Leadership": ["Project Management"],
        "Technical Proficiency": ["Technical Skills"],
        "Collaboration": ["Teamwork"]
    }

    # Generate a bar chart for competency level
    plt.figure(figsize=(10, 6))
    df.plot(x="Employee Name", y="Competency Level", kind='bar', color='#FFA07A')
    plt.title("Employee Competency Matrix")
    plt.xlabel("Employees")
    plt.ylabel("Competency Level")
    bar_chart_path = "/data/bar_chart.png"
    plt.savefig(bar_chart_path, format='png')
    plt.close()

    # Generate a heatmap for detailed skills
    plt.figure(figsize=(8, 6))
    heatmap_data = df.set_index("Employee Name").drop(columns=["Competency Level"])
    sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", cbar=True, fmt=".1f")
    heatmap_path = "/data/heatmap.png"
    plt.savefig(heatmap_path, format='png')
    plt.close()

    # Initialize PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Competency Matrix Report", ln=True, align="C")
    pdf.image(bar_chart_path, x=10, y=30, w=180)

    # Insert heatmap on a new page
    pdf.add_page()
    pdf.cell(200, 10, txt="Competency Level Heatmap", ln=True, align="C")
    pdf.image(heatmap_path, x=10, y=20, w=180)

    # Summarize skills in macro categories and identify improvement areas
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Summary of Skills and Areas for Improvement", ln=True, align="C")
    pdf.ln(10)

    improvement_threshold = 3  # Define threshold for identifying areas of improvement
    for _, row in df.iterrows():
        employee_name = row["Employee Name"]
        pdf.set_font("Arial", size=10, style='B')
        pdf.cell(200, 10, txt=f"{employee_name}", ln=True)
        pdf.set_font("Arial", size=10)

        strengths = []
        improvements = []

        for category, skills in categories.items():
            category_scores = [row[skill] for skill in skills if skill in row]
            avg_score = sum(category_scores) / len(category_scores) if category_scores else 0

            if avg_score >= improvement_threshold:
                strengths.append(f"{category} ({avg_score:.1f})")
            else:
                improvements.append(f"{category} ({avg_score:.1f})")

        summary_text = f"Strengths: {', '.join(strengths) if strengths else 'None'}\n"
        improvement_text = f"Areas for Improvement: {', '.join(improvements) if improvements else 'None'}\n"

        pdf.multi_cell(0, 10, txt=summary_text + improvement_text)
        pdf.ln(5)

    # Save PDF
    pdf_path = "/data/Competency_Matrix_Report.pdf"
    pdf.output(pdf_path)

    return {"message": "PDF generated successfully with charts and summaries!", "pdf_path": pdf_path}