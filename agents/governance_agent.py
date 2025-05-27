import pdfplumber

class GovernanceAgent:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def read_regulation(self):
        with pdfplumber.open(self.pdf_path) as pdf:
            return pdf.pages[0].extract_text()[:1000]  # Short summary for now
