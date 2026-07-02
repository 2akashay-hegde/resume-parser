from pathlib import Path
from typing import Optional

import fitz
import pdfplumber
from docx import Document


def extract_text(file_path: str) -> str:
    """Extract raw text from a PDF or DOCX file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return _extract_from_pdf(path)
    if suffix == ".docx":
        return _extract_from_docx(path)

    raise ValueError(f"Unsupported file type: {suffix}")


def _extract_from_pdf(path: Path) -> str:
    text_parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)

    if text_parts and any(part.strip() for part in text_parts):
        return "\n".join(part for part in text_parts if part).strip()

    doc = fitz.open(path)
    try:
        text_parts = [page.get_text() for page in doc]
    finally:
        doc.close()
    return "\n".join(part for part in text_parts if part).strip()


def _extract_from_docx(path: Path) -> str:
    document = Document(path)
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
    return "\n".join(paragraphs)
