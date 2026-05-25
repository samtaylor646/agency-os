import os

def extract_text(file_path: str, file_type: str) -> str:
    """Extracts text from a document based on its file type."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    if file_type == 'pdf':
        return _extract_pdf(file_path)
    elif file_type == 'docx':
        return _extract_docx(file_path)
    elif file_type in ['md', 'txt']:
        return _extract_text_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

def _extract_pdf(file_path: str) -> str:
    try:
        import PyPDF2
        text = []
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text.append(page.extract_text() or "")
        return "\n".join(text)
    except ImportError:
        return "PyPDF2 not installed. Mock extraction for PDF."

def _extract_docx(file_path: str) -> str:
    try:
        import docx
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except ImportError:
        return "python-docx not installed. Mock extraction for DOCX."

def _extract_text_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
