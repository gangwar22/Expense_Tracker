import React from "react";

export default function Navbar({ onOpenAddModal, onExport, backendOnline }) {
  return (
    <header className="navbar">
      <div className="navbar-container">
        <div className="logo-group">
          <div className="logo-icon">💰</div>
          <div>
            <h1 className="logo-title">ExpenseTracker</h1>
            <p className="logo-subtitle">FastAPI & React Dashboard</p>
          </div>
        </div>

        <div className="nav-actions">
          <div className={`status-badge ${backendOnline ? "online" : "offline"}`}>
            <span className="status-dot"></span>
            {backendOnline ? "API Connected" : "Connecting..."}
          </div>

          <button
            id="export-csv-btn"
            className="btn btn-secondary"
            onClick={onExport}
            title="Download CSV report"
          >
            📥 Export CSV
          </button>

          <button
            id="add-expense-btn"
            className="btn btn-primary"
            onClick={onOpenAddModal}
          >
            ➕ Add Expense
          </button>
        </div>
      </div>
    </header>
  );
}
