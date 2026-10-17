"""
FastAPI Main Application
Defines all API routes (endpoints), error handling, and server configuration.
Simple, clean, and beginner-friendly structure!
"""
from typing import List, Optional, Dict
from fastapi import FastAPI, Request, Query, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.models import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
    StatisticsResponse,
)
from app.services import expense_service
from app.analytics import expense_analytics

# Initialize the FastAPI app
app = FastAPI(
    title="Expense Tracker API",
    description="A simple and clean REST API to track daily expenses using FastAPI, Pandas, and NumPy.",
    version="1.0.0",
)

# Enable CORS (Cross-Origin Resource Sharing) so web clients can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Error Handlers
# ==========================================
@app.exception_handler(ValueError)
async def handle_value_error(request: Request, exc: ValueError):
    """Handles bad inputs and validation errors with 400 Bad Request."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


@app.exception_handler(RequestValidationError)
async def handle_validation_error(request: Request, exc: RequestValidationError):
    """Formats Pydantic validation errors clearly with 422 status."""
    error_messages = [
        f"{'.'.join(str(loc) for loc in err.get('loc', []))}: {err.get('msg')}"
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"detail": error_messages},
    )


# ==========================================
# 1. Welcome / Home Route
# ==========================================
@app.get("/", tags=["Home"])
def home():
    """Welcome route with links to docs and available endpoints."""
    return {
        "message": "Welcome to Expense Tracker API",
        "docs_url": "/docs",
        "endpoints": {
            "all_expenses": "/expenses",
            "monthly_report": "/reports/monthly",
            "category_report": "/reports/category",
            "statistics_report": "/reports/statistics",
            "export_csv": "/reports/export",
        },
    }


# ==========================================
# 2. Expense CRUD Routes
# ==========================================
@app.post("/expenses", status_code=status.HTTP_201_CREATED, tags=["Expenses"])
def add_expense(expense_data: ExpenseCreate):
    """
    Add a new expense.
    Takes title, amount, category, date, and optional notes.
    """
    new_expense = expense_service.create(expense_data)
    return {
        "message": "Expense added successfully",
        "expense": new_expense.to_dict(),
    }


@app.get("/expenses", response_model=List[ExpenseResponse], tags=["Expenses"])
def get_all_expenses(
    category: Optional[str] = Query(None, description="Search by category name"),
    date: Optional[str] = Query(None, description="Search by exact date (YYYY-MM-DD)"),
    start_date: Optional[str] = Query(None, description="Filter from start date"),
    end_date: Optional[str] = Query(None, description="Filter up to end date"),
    sort_by: Optional[str] = Query("id", description="Sort column: id, title, amount, category, date"),
    order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, description="Maximum items to return"),
):
    """
    Retrieve all expenses with optional filtering, sorting, and pagination.
    """
    expenses = expense_service.get_all(
        category=category,
        date_str=date,
        start_date=start_date,
        end_date=end_date,
        sort_by=sort_by or "id",
        order=order or "asc",
        skip=skip,
        limit=limit,
    )
    return [e.to_dict() for e in expenses]


@app.get("/expenses/{expense_id}", response_model=ExpenseResponse, tags=["Expenses"])
def get_expense_by_id(expense_id: int):
    """
    Fetch a single expense by its ID. Returns 404 if not found.
    """
    expense = expense_service.get_by_id(expense_id)
    return expense.to_dict()


@app.put("/expenses/{expense_id}", tags=["Expenses"])
def update_expense(expense_id: int, expense_data: ExpenseUpdate):
    """
    Update fields of an existing expense by ID.
    """
    updated_expense = expense_service.update(expense_id, expense_data)
    return {
        "message": "Expense updated successfully",
        "expense": updated_expense.to_dict(),
    }


@app.delete("/expenses/{expense_id}", tags=["Expenses"])
def delete_expense(expense_id: int):
    """
    Delete an expense from CSV by ID.
    """
    expense_service.delete(expense_id)
    return {
        "message": "Expense deleted successfully",
        "id": expense_id,
    }


# ==========================================
# 3. Analytics & Reporting Routes
# ==========================================
@app.get("/reports/monthly", response_model=Dict[str, float], tags=["Reports"])
def monthly_report():
    """Returns monthly spending breakdown using Pandas (e.g. {'September': 4200.0})."""
    return expense_analytics.get_monthly_summary()


@app.get("/reports/category", response_model=Dict[str, float], tags=["Reports"])
def category_report():
    """Returns category-wise spending breakdown using Pandas."""
    return expense_analytics.get_category_summary()


@app.get("/reports/statistics", response_model=StatisticsResponse, tags=["Reports"])
def overall_statistics():
    """Returns total, average, highest, lowest, and count using NumPy."""
    return expense_analytics.get_overall_statistics()


@app.get("/reports/export", tags=["Reports"])
def export_csv():
    """Bonus: Download all expenses as a CSV file."""
    return FileResponse(
        path=expense_service.file_path,
        media_type="text/csv",
        filename="expenses_export.csv",
    )
