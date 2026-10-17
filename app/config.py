"""
Configuration File
Stores file paths and settings for the Expense Tracker.
"""
import os
from pathlib import Path

# Base folder of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Path to the data folder and CSV file
DATA_DIR = BASE_DIR / "data"
CSV_FILE_PATH = Path(os.getenv("EXPENSES_CSV_PATH", str(DATA_DIR / "expenses.csv")))

# CSV column headers
CSV_HEADERS = ["id", "title", "amount", "category", "date", "notes"]
