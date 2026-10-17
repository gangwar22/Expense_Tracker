"""
Comprehensive Automated Tests for Expense Tracker API
Tests all CRUD operations, analytics reports, validation errors, and bonus features.
"""
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
import csv

from app.main import app
from app.services import ExpenseService, expense_service
from app.analytics import ExpenseAnalytics, expense_analytics


@pytest.fixture(autouse=True)
def setup_test_csv(tmp_path: Path, monkeypatch):
    """
    Creates an isolated test CSV with sample expenses for each test function.
    Points both service and analytics to this temporary file.
    """
    test_csv = tmp_path / "test_expenses.csv"
    headers = ["id", "title", "amount", "category", "date", "notes"]

    # Initial test dataset
    rows = [
        {"id": 1, "title": "Lunch", "amount": 250.0, "category": "Food", "date": "2026-09-20", "notes": "Office lunch"},
        {"id": 2, "title": "Travel Metro", "amount": 120.0, "category": "Travel", "date": "2026-09-20", "notes": "Commute"},
        {"id": 3, "title": "Shopping Shoes", "amount": 800.0, "category": "Shopping", "date": "2026-09-21", "notes": "Sneakers"},
        {"id": 4, "title": "Dinner Pizza", "amount": 950.0, "category": "Food", "date": "2026-09-22", "notes": "Dinner with team"},
    ]

    with open(test_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    # Monkeypatch the service and analytics instances to use the test CSV
    monkeypatch.setattr(expense_service, "file_path", test_csv)
    monkeypatch.setattr(expense_analytics, "file_path", test_csv)
    yield test_csv


@pytest.fixture
def client():
    return TestClient(app)


# ==========================================
# 1. Root & Discovery Tests
# ==========================================
def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs_url" in data
    assert data["docs_url"] == "/docs"


# ==========================================
# 2. Core CRUD Tests
# ==========================================
def test_get_all_expenses(client):
    response = client.get("/expenses")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 4
    assert data[0]["title"] == "Lunch"
    assert data[0]["amount"] == 250.0


def test_get_expense_by_id_success(client):
    response = client.get("/expenses/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Lunch"
    assert data["amount"] == 250.0
    assert data["category"] == "Food"


def test_get_expense_by_id_not_found(client):
    response = client.get("/expenses/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_add_expense_success(client):
    new_expense = {
        "title": "Coffee",
        "amount": 120.0,
        "category": "Food",
        "date": "2026-09-25",
        "notes": "Cafe"
    }
    response = client.post("/expenses", json=new_expense)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Expense added successfully"
    assert data["expense"]["id"] == 5
    assert data["expense"]["title"] == "Coffee"
    assert data["expense"]["amount"] == 120.0

    # Verify persisted in storage
    get_res = client.get("/expenses/5")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "Coffee"


def test_update_expense_success(client):
    update_payload = {
        "title": "Executive Lunch Buffet",
        "amount": 350.0,
        "notes": "Updated notes"
    }
    response = client.put("/expenses/1", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Expense updated successfully"
    assert data["expense"]["title"] == "Executive Lunch Buffet"
    assert data["expense"]["amount"] == 350.0
    assert data["expense"]["category"] == "Food"  # Preserved unchanged

    # Verify persisted
    get_res = client.get("/expenses/1")
    assert get_res.json()["title"] == "Executive Lunch Buffet"


def test_update_expense_not_found(client):
    response = client.put("/expenses/9999", json={"title": "Ghost"})
    assert response.status_code == 404


def test_delete_expense_success(client):
    response = client.delete("/expenses/1")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Expense deleted successfully"
    assert data["id"] == 1

    # Verify it is deleted
    get_res = client.get("/expenses/1")
    assert get_res.status_code == 404


def test_delete_expense_not_found(client):
    response = client.delete("/expenses/9999")
    assert response.status_code == 404


# ==========================================
# 3. Validation & Error Handling Tests
# ==========================================
def test_add_expense_invalid_amount(client):
    # Amount <= 0
    payload = {
        "title": "Free item",
        "amount": -50.0,
        "category": "Food",
        "date": "2026-09-25"
    }
    response = client.post("/expenses", json=payload)
    assert response.status_code == 422


def test_add_expense_zero_amount(client):
    payload = {
        "title": "Zero item",
        "amount": 0,
        "category": "Food",
        "date": "2026-09-25"
    }
    response = client.post("/expenses", json=payload)
    assert response.status_code == 422


def test_add_expense_empty_title(client):
    payload = {
        "title": "   ",
        "amount": 100.0,
        "category": "Food",
        "date": "2026-09-25"
    }
    response = client.post("/expenses", json=payload)
    assert response.status_code == 422


def test_add_expense_invalid_date(client):
    payload = {
        "title": "Snacks",
        "amount": 100.0,
        "category": "Food",
        "date": "not-a-date"
    }
    response = client.post("/expenses", json=payload)
    assert response.status_code == 422


def test_add_expense_missing_required_fields(client):
    # Missing title and category
    payload = {
        "amount": 100.0,
        "date": "2026-09-25"
    }
    response = client.post("/expenses", json=payload)
    assert response.status_code == 422


# ==========================================
# 4. Analytics & Reports Tests
# ==========================================
def test_monthly_report(client):
    response = client.get("/reports/monthly")
    assert response.status_code == 200
    data = response.json()
    # Total for September: 250 + 120 + 800 + 950 = 2120
    assert "September" in data
    assert data["September"] == 2120.0


def test_category_report(client):
    response = client.get("/reports/category")
    assert response.status_code == 200
    data = response.json()
    # Food: 250 + 950 = 1200
    # Travel: 120
    # Shopping: 800
    assert data["Food"] == 1200.0
    assert data["Travel"] == 120.0
    assert data["Shopping"] == 800.0


def test_statistics_report(client):
    response = client.get("/reports/statistics")
    assert response.status_code == 200
    data = response.json()
    # Total: 2120.0, count: 4, average: 530.0, highest: 950.0, lowest: 120.0
    assert data["total"] == 2120.0
    assert data["count"] == 4
    assert data["average"] == 530.0
    assert data["highest"] == 950.0
    assert data["lowest"] == 120.0


# ==========================================
# 5. Bonus Features Tests
# ==========================================
def test_search_by_category(client):
    response = client.get("/expenses?category=Food")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for exp in data:
        assert exp["category"] == "Food"


def test_search_by_date(client):
    response = client.get("/expenses?date=2026-09-20")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for exp in data:
        assert exp["date"] == "2026-09-20"


def test_search_by_date_range(client):
    response = client.get("/expenses?start_date=2026-09-21&end_date=2026-09-22")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    dates = {exp["date"] for exp in data}
    assert dates == {"2026-09-21", "2026-09-22"}


def test_sorting_by_amount_desc(client):
    response = client.get("/expenses?sort_by=amount&order=desc")
    assert response.status_code == 200
    data = response.json()
    amounts = [exp["amount"] for exp in data]
    assert amounts == [950.0, 800.0, 250.0, 120.0]


def test_pagination(client):
    response = client.get("/expenses?skip=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == 2
    assert data[1]["id"] == 3


def test_export_report_csv(client):
    response = client.get("/reports/export")
    assert response.status_code == 200
    assert "text/csv" in response.headers.get("content-type", "")
    assert "attachment" in response.headers.get("content-disposition", "")
    assert b"id,title,amount,category,date,notes" in response.content
