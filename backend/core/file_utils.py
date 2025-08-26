"""
File management utilities
"""
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import re
from .config import ALLOWED_DOCUMENT_EXTENSIONS, OUTPUT_EXTENSIONS


def sanitize_ticker(ticker: str) -> str:
    """Sanitize ticker symbol for use in file paths"""
    return re.sub(r'[^A-Za-z0-9]', '', ticker).upper()


def list_files_in_directory(directory: Path, extensions: List[str]) -> List[Dict[str, Any]]:
    """
    List files in a directory with specified extensions
    
    Args:
        directory: Path to the directory
        extensions: List of allowed file extensions
    
    Returns:
        List of file information dictionaries
    """
    if not directory.exists():
        return []
    
    files = []
    for file in directory.iterdir():
        if file.is_file() and file.suffix in extensions:
            files.append({
                "name": file.name,
                "size": file.stat().st_size,
                "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })
    
    return sorted(files, key=lambda x: x["modified"], reverse=True)


def save_file_with_timestamp(file_path: Path, content: bytes) -> Path:
    """
    Save a file with timestamp if it already exists
    
    Args:
        file_path: Desired file path
        content: File content to write
    
    Returns:
        Actual path where file was saved
    """
    if file_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stem = file_path.stem
        suffix = file_path.suffix
        file_path = file_path.parent / f"{stem}_{timestamp}{suffix}"
    
    with open(file_path, 'wb') as f:
        f.write(content)
    
    return file_path


def save_text_file_with_timestamp(file_path: Path, content: str) -> Path:
    """
    Save a text file with timestamp if it already exists
    
    Args:
        file_path: Desired file path
        content: Text content to write
    
    Returns:
        Actual path where file was saved
    """
    if file_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stem = file_path.stem
        suffix = file_path.suffix
        file_path = file_path.parent / f"{stem}_{timestamp}{suffix}"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return file_path


def read_markdown_file(file_path: Path) -> Optional[str]:
    """
    Read a markdown file content
    
    Args:
        file_path: Path to the markdown file
    
    Returns:
        File content or None if not found or not markdown
    """
    if not file_path.exists() or not file_path.is_file():
        return None
    
    if file_path.suffix == '.md':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    return None


def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Validate file extension against allowed list
    
    Args:
        filename: Name of the file
        allowed_extensions: List of allowed extensions
    
    Returns:
        True if extension is valid, False otherwise
    """
    file_ext = Path(filename).suffix.lower()
    return file_ext in allowed_extensions