# report_generator.py

import os
from fpdf import FPDF
from app.config import VISUALS_PATH, REPORT_PATH
import re

def remove_emojis(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, remove_emojis("Auto Data Visualizer Report"), ln=True, align="C")
        self.ln(10)

    def add_image(self, img_path, label):
        self.set_font("Arial", "B", 12)
        self.multi_cell(0, 10, remove_emojis(label))
        if os.path.exists(img_path):
            self.image(img_path, w=180)
            self.ln()

def generate_pdf_report():
    pdf = PDFReport()
    pdf.add_page()

    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, remove_emojis("This report contains visualized insights from the dataset after cleaning and outlier removal."))
    pdf.ln()

    for img_file in sorted(os.listdir(VISUALS_PATH)):
        if img_file.endswith(".png"):
            label = os.path.splitext(img_file)[0].replace('_', ' ').title()
            img_path = os.path.join(VISUALS_PATH, img_file)
            pdf.add_image(img_path, label)

    pdf.output(REPORT_PATH)
    return REPORT_PATH
