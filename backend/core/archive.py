"""
Archive management functionality
"""
from pathlib import Path
from datetime import datetime
import shutil
from typing import Optional, List, Dict, Any
from .config import ARCHIVE_DIR, OUTPUT_DIR, OUTPUT_EXTENSIONS


def archive_outputs(output_path: Path, archive_path: Path) -> Optional[str]:
    """
    Archive existing output files before new analysis
    
    Args:
        output_path: Path to the output directory
        archive_path: Path to the archive directory
    
    Returns:
        Timestamp string if files were archived, None otherwise
    """
    if not output_path.exists():
        return None
    
    # Create archive directory if it doesn't exist
    archive_path.mkdir(parents=True, exist_ok=True)
    
    # Create timestamped subdirectory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_subdir = archive_path / timestamp
    archive_subdir.mkdir(exist_ok=True)
    
    # Move all files from output to archive
    files_archived = False
    for file in output_path.iterdir():
        if file.is_file() and file.suffix in OUTPUT_EXTENSIONS:
            shutil.move(str(file), str(archive_subdir / file.name))
            files_archived = True
    
    # Also move any subdirectories
    for subdir in output_path.iterdir():
        if subdir.is_dir() and subdir.name != '__pycache__':
            shutil.move(str(subdir), str(archive_subdir / subdir.name))
            files_archived = True
    
    return timestamp if files_archived else None


def archive_existing_outputs() -> Optional[str]:
    """Archive existing output files before new analysis"""
    return archive_outputs(OUTPUT_DIR, ARCHIVE_DIR)


def archive_company_outputs(ticker: str) -> Optional[str]:
    """Archive existing output files for a specific company before new analysis"""
    output_path = OUTPUT_DIR / "companies" / ticker
    archive_path = ARCHIVE_DIR / "companies" / ticker
    return archive_outputs(output_path, archive_path)


def list_archives(archive_path: Path) -> List[Dict[str, Any]]:
    """
    List all archives in a directory
    
    Args:
        archive_path: Path to the archive directory
    
    Returns:
        List of archive information dictionaries
    """
    if not archive_path.exists():
        return []
    
    archives = []
    for folder in sorted(archive_path.iterdir(), reverse=True):
        if folder.is_dir():
            files = []
            for file in folder.iterdir():
                if file.suffix in OUTPUT_EXTENSIONS:
                    files.append({
                        "name": file.name,
                        "size": file.stat().st_size,
                        "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
                    })
            
            archives.append({
                "timestamp": folder.name,
                "date": datetime.strptime(folder.name, "%Y%m%d_%H%M%S").isoformat() if '_' in folder.name else folder.name,
                "files": files,
                "file_count": len(files)
            })
    
    return archives


def get_archive_file_content(archive_path: Path, timestamp: str, filename: str) -> Optional[str]:
    """
    Get content of an archived markdown file
    
    Args:
        archive_path: Base archive directory path
        timestamp: Archive timestamp
        filename: Name of the file
    
    Returns:
        File content if it's a markdown file, None otherwise
    """
    file_path = archive_path / timestamp / filename
    
    if not file_path.exists() or not file_path.is_file():
        return None
    
    if filename.endswith('.md'):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    return None