"""
Unit Tests for OOP Expense Domain Model
Verifies OOP encapsulation, domain validation rules, mutation, and serialization.
"""
import pytest
from datetime import date
from app.models import Expense


def test_expense_creation_valid():
    exp = Expense(
        id=1,
        title="Lunch",
        amount=250.0,
        category="Food",
        date="2026-09-25",
        notes="Office lunch",
    )
    assert exp.id == 1
    assert exp.title == "Lunch"
    assert exp.amount == 250.0
    assert exp.category == "Food"
    assert exp.date == "2026-09-25"
    assert exp.notes == "Office lunch"


def test_expense_creation_with_date_object():
    d = date(2026, 9, 25)
    exp = Expense(id=2, title="Metro", amount=80, category="travel", date=d)
    assert exp.date == "2026-09-25"
    assert exp.category == "Travel"  # Title-cased


def test_expense_invalid_id():
    with pytest.raises(ValueError, match="Expense ID must be a positive integer"):
        Expense(id=-1, title="Lunch", amount=100, category="Food", date="2026-09-25")


def test_expense_invalid_empty_title():
    with pytest.raises(ValueError, match="Expense title cannot be empty"):
        Expense(id=1, title="   ", amount=100, category="Food", date="2026-09-25")


def test_expense_invalid_negative_amount():
    with pytest.raises(ValueError, match="Expense amount must be greater than 0"):
        Expense(id=1, title="Lunch", amount=-50, category="Food", date="2026-09-25")


def test_expense_invalid_zero_amount():
    with pytest.raises(ValueError, match="Expense amount must be greater than 0"):
        Expense(id=1, title="Lunch", amount=0, category="Food", date="2026-09-25")


def test_expense_invalid_empty_category():
    with pytest.raises(ValueError, match="Expense category cannot be empty"):
        Expense(id=1, title="Lunch", amount=100, category="   ", date="2026-09-25")


def test_expense_invalid_date_format():
    with pytest.raises(ValueError, match="Invalid date format"):
        Expense(id=1, title="Lunch", amount=100, category="Food", date="25-09-2026")


def test_expense_update():
    exp = Expense(id=1, title="Lunch", amount=250.0, category="Food", date="2026-09-25")
    exp.update(title="Grand Dinner", amount=1200.0, category="Dining", notes="Anniversary")
    assert exp.title == "Grand Dinner"
    assert exp.amount == 1200.0
    assert exp.category == "Dining"
    assert exp.notes == "Anniversary"


def test_expense_serialization_roundtrip():
    data = {
        "id": 10,
        "title": "Books",
        "amount": 499.5,
        "category": "Education",
        "date": "2026-09-28",
        "notes": "Python book",
    }
    exp = Expense.from_dict(data)
    assert exp.to_dict() == data
