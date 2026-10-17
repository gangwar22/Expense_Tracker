"""
CRUD Operations & Services
Handles reading and writing expenses to the CSV file.
Very easy to understand and explain in an interview or exam!
"""
import csv
from pathlib import Path
from typing import List, Optional
from fastapi import HTTPException

from app.config import CSV_FILE_PATH, CSV_HEADERS
from app.models import Expense, ExpenseCreate, ExpenseUpdate
from app.utils import ensure_csv_file


class ExpenseService:
    """
    Service class to handle all CRUD actions:
    Create, Read, Update, Delete for Expenses in CSV.
    """

    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = file_path or CSV_FILE_PATH

    def _read_all(self) -> List[Expense]:
        """
        Step 1: Read all rows from expenses.csv
        Step 2: Convert each row into an Expense object
        Step 3: Return the list of Expense objects
        """
        ensure_csv_file(self.file_path)
        expenses = []

        with open(self.file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row and row.get("id"):
                    expense = Expense.from_dict(row)
                    expenses.append(expense)

        return expenses

    def _write_all(self, expenses: List[Expense]) -> None:
        """
        Write the entire list of Expense objects back into expenses.csv
        """
        ensure_csv_file(self.file_path)
        with open(self.file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            for exp in expenses:
                writer.writerow(exp.to_dict())

    def get_all(
        self,
        category: Optional[str] = None,
        date_str: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        sort_by: str = "id",
        order: str = "asc",
        skip: int = 0,
        limit: int = 100,
    ) -> List[Expense]:
        """
        Returns all expenses with optional search, sorting, and pagination.
        """
        expenses = self._read_all()

        # 1. Filter by category if provided
        if category:
            cat = category.strip().lower()
            expenses = [e for e in expenses if cat in e.category.lower()]

        # 2. Filter by exact date if provided
        if date_str:
            expenses = [e for e in expenses if e.date == date_str.strip()]

        # 3. Filter by date range (start_date to end_date)
        if start_date:
            expenses = [e for e in expenses if e.date >= start_date.strip()]
        if end_date:
            expenses = [e for e in expenses if e.date <= end_date.strip()]

        # 4. Sorting
        valid_fields = ["id", "title", "amount", "category", "date"]
        sort_field = sort_by if sort_by in valid_fields else "id"
        is_descending = (order.lower() == "desc")
        expenses.sort(key=lambda x: getattr(x, sort_field), reverse=is_descending)

        # 5. Pagination (skip and limit)
        return expenses[skip : skip + limit]

    def get_by_id(self, expense_id: int) -> Expense:
        """
        Find an expense by ID. If not found, raise a 404 error.
        """
        expenses = self._read_all()
        for exp in expenses:
            if exp.id == expense_id:
                return exp

        # If loop finishes without returning, expense wasn't found
        raise HTTPException(status_code=404, detail=f"Expense with id {expense_id} not found")

    def create(self, data: ExpenseCreate) -> Expense:
        """
        Add a new expense:
        1. Read existing expenses
        2. Calculate next ID (highest current ID + 1)
        3. Create new Expense object
        4. Append and save to CSV
        """
        expenses = self._read_all()

        # Calculate next auto-incrementing ID
        if expenses:
            next_id = max(e.id for e in expenses) + 1
        else:
            next_id = 1

        new_expense = Expense(
            id=next_id,
            title=data.title,
            amount=data.amount,
            category=data.category,
            date=data.date,
            notes=data.notes or "",
        )

        expenses.append(new_expense)
        self._write_all(expenses)
        return new_expense

    def update(self, expense_id: int, data: ExpenseUpdate) -> Expense:
        """
        Update an existing expense by ID.
        """
        expenses = self._read_all()
        target = None

        for exp in expenses:
            if exp.id == expense_id:
                target = exp
                break

        if not target:
            raise HTTPException(status_code=404, detail=f"Expense with id {expense_id} not found")

        # Update only fields that were sent in the request
        target.update(
            title=data.title,
            amount=data.amount,
            category=data.category,
            date=data.date,
            notes=data.notes,
        )

        self._write_all(expenses)
        return target

    def delete(self, expense_id: int) -> Expense:
        """
        Delete an expense by ID from CSV.
        """
        expenses = self._read_all()
        target = None

        for exp in expenses:
            if exp.id == expense_id:
                target = exp
                break

        if not target:
            raise HTTPException(status_code=404, detail=f"Expense with id {expense_id} not found")

        # Keep all expenses except the one to be deleted
        remaining_expenses = [e for e in expenses if e.id != expense_id]
        self._write_all(remaining_expenses)
        return target


# Create a single instance to be used across the app
expense_service = ExpenseService()
