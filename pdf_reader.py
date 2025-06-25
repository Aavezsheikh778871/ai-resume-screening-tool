import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Example usage:
pdf_path = r"C:\Users\firdosh.shaikh\AI Resume Screening Tool\resumes\sample.pdf"
print(extract_text_from_pdf(pdf_path))
