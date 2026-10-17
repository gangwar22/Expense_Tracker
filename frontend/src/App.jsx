import React, { useState, useEffect, useCallback } from "react";
import "./App.css";
import { api } from "./services/api";
import Navbar from "./components/Navbar";
import StatsCards from "./components/StatsCards";
import CategoryReport from "./components/CategoryReport";
import ExpenseList from "./components/ExpenseList";
import ExpenseModal from "./components/ExpenseModal";
import Toast from "./components/Toast";

export default function App() {
  const [expenses, setExpenses] = useState([]);
  const [stats, setStats] = useState({ total: 0, average: 0, highest: 0, count: 0, lowest: 0 });
  const [categories, setCategories] = useState({});
  const [monthly, setMonthly] = useState({});
  const [loading, setLoading] = useState(true);
  const [backendOnline, setBackendOnline] = useState(false);

  // Filters & Sorting
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [searchTerm, setSearchTerm] = useState("");
  const [sortBy, setSortBy] = useState("id-desc");

  // Modal & Toast
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingExpense, setEditingExpense] = useState(null);
  const [toast, setToast] = useState(null);

  const showToast = (message, type = "success") => {
    setToast({ message, type });
  };

  // Fetch all data from FastAPI
  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      // Split sort field and order
      const [field, order] = sortBy.split("-");

      const [expensesData, statsData, catData, monthData] = await Promise.all([
        api.getExpenses({
          category: selectedCategory,
          sortBy: field,
          order: order,
        }),
        api.getStatistics(),
        api.getCategoryReport(),
        api.getMonthlyReport(),
      ]);

      setExpenses(expensesData);
      setStats(statsData);
      setCategories(catData);
      setMonthly(monthData);
      setBackendOnline(true);
    } catch (err) {
      console.error("Error connecting to backend:", err);
      setBackendOnline(false);
      showToast("Cannot connect to FastAPI backend at http://127.0.0.1:8000", "error");
    } finally {
      setLoading(false);
    }
  }, [selectedCategory, sortBy]);

  // Initial load
  useEffect(() => {
    loadData();
  }, [loadData]);

  // Save Expense (Create or Update)
  const handleSaveExpense = async (expenseData) => {
    if (editingExpense) {
      await api.updateExpense(editingExpense.id, expenseData);
      showToast("Expense updated successfully!");
    } else {
      await api.createExpense(expenseData);
      showToast("New expense added successfully!");
    }
    loadData();
  };

  // Delete Expense
  const handleDeleteExpense = async (id) => {
    if (window.confirm(`Are you sure you want to delete expense #${id}?`)) {
      try {
        await api.deleteExpense(id);
        showToast("Expense deleted successfully!");
        loadData();
      } catch (err) {
        showToast(err.message, "error");
      }
    }
  };

  // Export CSV
  const handleExport = () => {
    const exportUrl = api.getExportUrl();
    window.location.href = exportUrl;
    showToast("Downloading expenses CSV export...");
  };

  return (
    <div className="app-container">
      {/* Toast Alert */}
      <Toast toast={toast} onClose={() => setToast(null)} />

      {/* Navigation Header */}
      <Navbar
        onOpenAddModal={() => {
          setEditingExpense(null);
          setIsModalOpen(true);
        }}
        onExport={handleExport}
        backendOnline={backendOnline}
      />

      <main className="main-content">
        {/* Backend offline warning banner */}
        {!backendOnline && (
          <div className="backend-alert-banner">
            ⚠️ <strong>Backend Not Connected:</strong> Please make sure your FastAPI server is running with{" "}
            <code>uvicorn app.main:app --reload</code> on port 8000.
          </div>
        )}

        {/* 1. Statistics Cards */}
        <section className="section-block">
          <StatsCards stats={stats} />
        </section>

        {/* 2. Visual Analytics (Category & Monthly) */}
        <section className="section-block">
          <CategoryReport
            categories={categories}
            monthly={monthly}
            totalAmount={stats.total || 0}
          />
        </section>

        {/* 3. Expense List with Search, Filter & Actions */}
        <section className="section-block">
          <ExpenseList
            expenses={expenses}
            loading={loading}
            selectedCategory={selectedCategory}
            onSelectCategory={setSelectedCategory}
            searchTerm={searchTerm}
            onSearchChange={setSearchTerm}
            sortBy={sortBy}
            onSortChange={setSortBy}
            onEdit={(exp) => {
              setEditingExpense(exp);
              setIsModalOpen(true);
            }}
            onDelete={handleDeleteExpense}
          />
        </section>
      </main>

      {/* Add / Edit Modal */}
      <ExpenseModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSave={handleSaveExpense}
        editingExpense={editingExpense}
      />

      {/* Footer */}
      <footer className="footer">
        <p>
          Expense Tracker API &copy; {new Date().getFullYear()} • Built with FastAPI, Pandas, NumPy, and React.
        </p>
      </footer>
    </div>
  );
}
