from pathlib import Path
from docx import Document
from PyPDF2 import PdfReader

def read_txt(path):

    try:

        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            return f.read(3000)

    except:
        return ""

def read_docx(path):

    try:

        doc = Document(path)

        text = "\n".join(
            p.text for p in doc.paragraphs
        )

        return text[:3000]

    except:
        return ""

def read_pdf(path):

    try:

        reader = PdfReader(path)

        text = ""

        for page in reader.pages[:3]:

            content = page.extract_text()

            if content:
                text += content

        return text[:3000]

    except:
        return ""

def get_file_content(path):

    ext = Path(path).suffix.lower()

    if ext == ".txt":
        return read_txt(path)

    elif ext == ".docx":
        return read_docx(path)

    elif ext == ".pdf":
        return read_pdf(path)

    return ""