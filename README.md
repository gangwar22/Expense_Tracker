# 💰 Expense Tracker

A full-stack personal expense tracking application with a **FastAPI** backend, **Pandas/NumPy** analytics, flat-file **CSV persistence**, and an interactive **React (Vite)** dashboard.

---

## ✨ Features

- **Full CRUD Operations**: Add, view, edit, and delete expenses with automatic ID generation and validation.
- **Search, Filter & Sort**: Filter by category or date range, search by keyword, and sort by date, amount, or title.
- **Analytics & Insights**: Instant Pandas/NumPy calculations for total expenditure, monthly breakdown, category distribution, and spending averages.
- **CSV Storage & Export**: Lightweight data storage in `expenses.csv` with one-click CSV report export.
- **Modern React Dashboard**: Clean UI for visualizing stats, managing transactions, and viewing analytics in real time.
- **Interactive API Documentation**: Auto-generated Swagger UI for testing endpoints directly.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, FastAPI, Uvicorn, Pydantic v2
- **Data & Analytics**: Pandas, NumPy, CSV
- **Frontend**: React 19, Vite, Modern CSS
- **Testing**: Pytest, HTTPX

---

## 📁 Project Structure

```text
Python_expense_Tracker/
├── app/
│   ├── main.py          # FastAPI application & route definitions
│   ├── models.py        # Pydantic schemas & OOP models
│   ├── services.py      # Thread-safe CRUD logic & CSV file persistence
│   ├── analytics.py     # Pandas & NumPy aggregation engine
│   ├── utils.py         # Helper utilities (date parsing, CSV headers)
│   └── config.py        # Project configurations & paths
├── data/
│   └── expenses.csv     # Persistent CSV data file
├── frontend/            # React (Vite) dashboard UI
│   ├── src/             # Components, pages, styles, and API service
│   └── package.json
├── tests/               # Automated test suite (Pytest + HTTPX)
├── requirements.txt     # Python backend dependencies
└── pytest.ini           # Pytest settings
```

---

## 🚀 Quick Start

### ⚡ One-Command Start (Both Backend & Frontend)

Start both FastAPI and the React Dashboard together with a single command:

```bash
python run.py
```
*(On Windows, you can also simply double-click [`start.bat`](file:///c:/Users/Manoj/Desktop/Python_expense_Tracker/start.bat))*

---

### Manual Start (Separate Terminals)

#### 1. Backend Setup (FastAPI)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API server:**
   ```bash
   uvicorn app.main:app --reload
   ```

- **API URL**: `http://127.0.0.1:8000`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`
- **ReDoc Documentation**: `http://127.0.0.1:8000/redoc`

---

### 2. Frontend Setup (React Dashboard)

1. **Navigate to the frontend folder:**
   ```bash
   cd frontend
   ```

2. **Install dependencies and start development server:**
   ```bash
   npm install
   npm run dev
   ```

- **Dashboard UI**: `http://localhost:5173`

---

## 📡 API Endpoints

Interactive testing and schemas are available at [`/docs`](http://127.0.0.1:8000/docs).

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API status and overview |
| `POST` | `/expenses` | Create a new expense |
| `GET` | `/expenses` | List expenses (supports `category`, `date`, `sort_by`, `order`, `skip`, `limit`) |
| `GET` | `/expenses/{id}` | Get details of a single expense |
| `PUT` | `/expenses/{id}` | Update an existing expense |
| `DELETE` | `/expenses/{id}` | Delete an expense by ID |
| `GET` | `/reports/monthly` | Get spending aggregated by month |
| `GET` | `/reports/category` | Get spending distribution by category |
| `GET` | `/reports/statistics` | Get statistical metrics (total, average, highest, lowest, count) |
| `GET` | `/reports/export` | Download full expenses data as a CSV file |

---

## 🧪 Running Tests

Run the backend test suite:

```bash
pytest
```
