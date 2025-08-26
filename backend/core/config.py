"""
Shared configuration and constants for the backend
"""
from pathlib import Path
from typing import List

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
BACKEND_DIR = BASE_DIR / "backend"
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
ARCHIVE_DIR = BASE_DIR / "archive"
CONFIG_DIR = SRC_DIR / "xp_power_demo" / "config"

# CORS configuration
CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5173"]

# File extensions
ALLOWED_DOCUMENT_EXTENSIONS = ['.md', '.pdf', '.txt', '.csv', '.xlsx', '.docx']
OUTPUT_EXTENSIONS = ['.md', '.pdf']

# Analysis task names
ANALYSIS_TASKS = [
    "Analyzing primary ratios",
    "Checking ownership structure",
    "Evaluating earnings quality",
    "Assessing balance sheet durability",
    "Making investment decision"
]

# Multi-company limits
MAX_COMPANIES_PER_ANALYSIS = 10
MAX_PARALLEL_WORKERS = 3