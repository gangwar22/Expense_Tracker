"""
Helper Functions
Simple helper functions for file handling and date formatting.
"""
import csv
from pathlib import Path
from app.config import CSV_FILE_PATH, CSV_HEADERS


def ensure_csv_file(file_path: Path = None):
    """
    Checks if expenses.csv exists. If not, creates the folder
    and writes the header row: id, title, amount, category, date, notes.
    """
    path = file_path or CSV_FILE_PATH
    
    # Create folder if it doesn't exist
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # If file does not exist, create it with column headers
    if not path.exists() or path.stat().st_size == 0:
        with open(path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)
