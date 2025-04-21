# utils/extract_docx.py
import os
from docx import Document

def extract_all_docx_from_folder(folder_path):
    """
    Klasör içindeki tüm .docx dosyalarını (alt klasörler dahil) okur.
    """
    all_docs = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".docx"):
                file_path = os.path.join(root, file)
                doc = Document(file_path)
                text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
                all_docs.append({
                    "filename": file,
                    "text": text
                })

    return all_docs

import unicodedata

def fix_filename(name):
    return unicodedata.normalize("NFC", name)
