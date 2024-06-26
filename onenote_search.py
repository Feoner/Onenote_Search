import fitz  # pip install PyMuPDF
import re
import pandas as pd
from fpdf import FPDF

# Define specific patterns to search for update as needed
patterns = {
    'common_api_key': r'\b[A-Za-z0-9_]{40}\b',
    'jwt': r'\b[A-Za-z0-9_]{32}\.[A-Za-z0-9_]{182}\.[A-Za-z0-9_]{43}\b',
    'base64_token': r'\b[A-Za-z0-9+/]{40}==\b',
    'generic_secret_20': r'\b[A-Za-z0-9_]{20}\b',
    'generic_secret_30': r'\b[A-Za-z0-9_]{30}\b',
    'username': r'\buser(?:name)?\s*[:=]\s*\S+',
    'password': r'\bpass(?:word)?\s*[:=]\s*\S+',
    'secret': r'\bsecret\s*[:=]\s*\S+',
    'token': r'\btoken\s*[:=]\s*\S+',
}

def search_content(file_path):
    findings = []
    # Open the PDF file
    doc = fitz.open(file_path)
    for page in doc:
        content = page.get_text()
        for key, pattern in patterns.items():
            for match in re.finditer(pattern, content, re.IGNORECASE):
                findings.append({
                    'Type': key,
                    'Content': match.group(),
                    'Location': f"Page {page.number}, Position: {match.start()}"
                })
    doc.close()
    return findings



def generate_reports(results):
    df = pd.DataFrame(results)
    df.to_html('report.html')
    df.to_csv('report.csv')
    
    # PDF generation using FPDF
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Sensitive Data Report', 0, 1, 'C')
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    line_height = pdf.font_size * 2.5
    col_width = (pdf.w - pdf.l_margin - pdf.r_margin) / 4  # distribute content evenly across 4 columns

    for index, row in df.iterrows():
        pdf.cell(col_width, line_height, str(row['Type']), border=1)
        pdf.cell(col_width * 3, line_height, str(row['Content']) + " - " + str(row['Location']), border=1)
        pdf.ln(line_height)

    pdf.output("report.pdf")


# Main execution
file_path = 'Path/to/notebook' # Update based on where your notebook is stored, this will need to be local
results = search_content(file_path)
if results:
    generate_reports(results)
else:
    print("No sensitive information found.")
