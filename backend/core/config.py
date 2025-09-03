"""
Shared configuration and constants for the backend
"""
import os
from pathlib import Path
from typing import List

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
BACKEND_DIR = BASE_DIR / "backend"
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
ARCHIVE_DIR = BASE_DIR / "archive"
CONFIG_DIR = SRC_DIR / "insig_analyst_demo" / "config"

# Server configuration
BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "3000"))
VITE_PORT = int(os.getenv("VITE_PORT", "5173"))

# CORS configuration
CORS_ORIGINS = [
    f"http://localhost:{FRONTEND_PORT}",
    f"http://localhost:{VITE_PORT}"
]

# Task management
MAX_TASKS = int(os.getenv("MAX_TASKS", "1000"))  # Maximum tasks in memory
TASK_RETENTION_HOURS = int(os.getenv("TASK_RETENTION_HOURS", "24"))  # Hours to keep tasks
TASK_TIMEOUT_MINUTES = int(os.getenv("TASK_TIMEOUT_MINUTES", "30"))  # Task timeout

# File extensions
ALLOWED_DOCUMENT_EXTENSIONS = ['.md', '.pdf', '.txt', '.csv', '.xlsx', '.docx']
OUTPUT_EXTENSIONS = ['.md', '.pdf']

# File upload limits
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", str(100 * 1024 * 1024)))  # 100MB default

# Analysis task names
ANALYSIS_TASKS = [
    "Analyzing primary ratios",
    "Checking ownership structure",
    "Evaluating earnings quality",
    "Assessing balance sheet durability",
    "Making investment decision"
]

