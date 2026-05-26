import os
from typing import List
import re

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

def sanitize_text(text: str) -> str:
    """
    Sanitizes text to prevent data poisoning and malformed embeddings.
    - Removes null bytes and non-printable control characters.
    - Normalizes whitespace.
    - Strips special LLM tokens that might be used for injection.
    """
    if not text:
        return ""
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Remove control characters except standard whitespace
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    
    # Remove common injection tokens (e.g., OpenAI special tokens)
    special_tokens = ["<|endoftext|>", "<|fim_prefix|>", "<|fim_middle|>", "<|fim_suffix|>", "<|endofprompt|>"]
    for token in special_tokens:
        text = text.replace(token, "")
        
    # Normalize whitespace (collapse multiple spaces/newlines)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Splits text into chunks of roughly `chunk_size` tokens/words with `overlap`.
    Uses a simple word-based splitting approach and sanitizes each chunk.
    """
    # Sanitize before chunking to ensure clean word splitting
    sanitized_text = sanitize_text(text)
    words = sanitized_text.split()
    chunks = []
    
    if not words:
        return []
        
    i = 0
    while i < len(words):
        chunk_words = words[i:i + chunk_size]
        chunks.append(" ".join(chunk_words))
        i += (chunk_size - overlap)
        
    return chunks
