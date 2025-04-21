# utils/extract_pdf.py
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text


"""
#kullanımı

from utils.extract_pdf import extract_text_from_pdf

metin = extract_text_from_pdf("dosyalar/kitap.pdf")
print(metin[:500])



"""