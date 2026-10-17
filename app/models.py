"""
Data Models and OOP Design
1. Expense Class: Standard Object-Oriented Class to manage expense data.
2. Pydantic Schemas: Used by FastAPI to validate incoming and outgoing JSON data.
"""
from typing import Optional, Dict, Any, Union
from datetime import date as dt_date, datetime
from pydantic import BaseModel, Field, field_validator


# ==========================================
# 1. OOP Domain Model (Expense Class)
# ==========================================
class Expense:
    """
    Object-Oriented Expense Class.
    Stores expense information and validates fields.
    """

    def __init__(
        self,
        id: int,
        title: str,
        amount: float,
        category: str,
        date: Union[dt_date, str],
        notes: str = "",
    ):
        # Validate ID
        if not isinstance(id, int) or id <= 0:
            raise ValueError(f"Expense ID must be a positive integer, got '{id}'.")
        self.id = id

        # Validate Title
        clean_title = str(title).strip()
        if not clean_title:
            raise ValueError("Expense title cannot be empty.")
        self.title = clean_title

        # Validate Amount
        try:
            amt = float(amount)
        except (ValueError, TypeError):
            raise ValueError("Expense amount must be a number.")
        if amt <= 0:
            raise ValueError("Expense amount must be greater than 0.")
        self.amount = round(amt, 2)

        # Validate Category
        clean_category = str(category).strip().title()
        if not clean_category:
            raise ValueError("Expense category cannot be empty.")
        self.category = clean_category

        # Validate Date format (YYYY-MM-DD)
        if isinstance(date, dt_date):
            self.date = date.isoformat()
        elif isinstance(date, str):
            clean_date = date.strip()
            try:
                datetime.strptime(clean_date, "%Y-%m-%d")
                self.date = clean_date
            except ValueError:
                raise ValueError(f"Invalid date format '{date}'. Expected YYYY-MM-DD.")
        else:
            raise ValueError("Date must be a date object or string in YYYY-MM-DD format.")

        # Notes (optional)
        self.notes = str(notes or "").strip()

    def update(
        self,
        title: Optional[str] = None,
        amount: Optional[float] = None,
        category: Optional[str] = None,
        date: Optional[Union[dt_date, str]] = None,
        notes: Optional[str] = None,
    ):
        """Update expense fields if new values are provided."""
        if title is not None and title.strip():
            self.title = title.strip()
        if amount is not None:
            if float(amount) <= 0:
                raise ValueError("Expense amount must be greater than 0.")
            self.amount = round(float(amount), 2)
        if category is not None and category.strip():
            self.category = category.strip().title()
        if date is not None:
            if isinstance(date, dt_date):
                self.date = date.isoformat()
            else:
                datetime.strptime(str(date).strip(), "%Y-%m-%d")
                self.date = str(date).strip()
        if notes is not None:
            self.notes = str(notes).strip()

    def to_dict(self) -> Dict[str, Any]:
        """Convert object into dictionary format for CSV and JSON responses."""
        return {
            "id": self.id,
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Expense":
        """Create an Expense object from a dictionary."""
        return cls(
            id=int(data["id"]),
            title=str(data["title"]),
            amount=float(data["amount"]),
            category=str(data["category"]),
            date=str(data["date"]),
            notes=str(data.get("notes", "")),
        )


# ==========================================
# 2. Pydantic Models for FastAPI Validation
# ==========================================
class ExpenseCreate(BaseModel):
    """Schema for adding a new expense via POST /expenses."""
    title: str = Field(..., min_length=1, description="Expense name/title")
    amount: float = Field(..., gt=0, description="Amount (must be greater than 0)")
    category: str = Field(..., min_length=1, description="Category name (e.g. Food)")
    date: dt_date = Field(..., description="Date in YYYY-MM-DD format")
    notes: Optional[str] = Field(default="", description="Optional remarks")

    @field_validator("title")
    @classmethod
    def check_title(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator("category")
    @classmethod
    def check_category(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Category cannot be empty")
        return v.strip().title()


class ExpenseUpdate(BaseModel):
    """Schema for updating an existing expense via PUT /expenses/{id}."""
    title: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None
    date: Optional[dt_date] = None
    notes: Optional[str] = None

    @field_validator("title")
    @classmethod
    def check_update_title(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip() if v else None

    @field_validator("amount")
    @classmethod
    def check_update_amount(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v


class ExpenseResponse(BaseModel):
    """Schema for returning expense details in API responses."""
    id: int
    title: str
    amount: float
    category: str
    date: str
    notes: str


class StatisticsResponse(BaseModel):
    """Schema for /reports/statistics endpoint."""
    total: float
    average: float
    highest: float
    count: int
    lowest: float = 0.0
