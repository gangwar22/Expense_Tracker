import React, { useState } from "react";

const CATEGORY_COLORS = {
  Food: { bg: "rgba(239, 68, 68, 0.15)", text: "#f87171", icon: "🍔" },
  Travel: { bg: "rgba(59, 130, 246, 0.15)", text: "#60a5fa", icon: "🚗" },
  Shopping: { bg: "rgba(236, 72, 153, 0.15)", text: "#f472b6", icon: "🛍️" },
  Bills: { bg: "rgba(245, 158, 11, 0.15)", text: "#fbbf24", icon: "💡" },
  Health: { bg: "rgba(16, 185, 129, 0.15)", text: "#34d399", icon: "💊" },
  Education: { bg: "rgba(168, 85, 247, 0.15)", text: "#c084fc", icon: "📚" },
  Entertainment: { bg: "rgba(14, 165, 233, 0.15)", text: "#38bdf8", icon: "🎬" },
};

export default function ExpenseList({
  expenses,
  loading,
  selectedCategory,
  onSelectCategory,
  searchTerm,
  onSearchChange,
  sortBy,
  onSortChange,
  onEdit,
  onDelete,
}) {
  const categories = ["All", "Food", "Travel", "Shopping", "Bills", "Health", "Education", "Entertainment"];

  // Filter based on search input (title or notes)
  const filteredExpenses = expenses.filter((e) => {
    const term = searchTerm.toLowerCase();
    const matchesTitle = e.title.toLowerCase().includes(term);
    const matchesNotes = (e.notes || "").toLowerCase().includes(term);
    const matchesCategory = e.category.toLowerCase().includes(term);
    return matchesTitle || matchesNotes || matchesCategory;
  });

  return (
    <div className="expense-list-section">
      <div className="section-header">
        <div>
          <h2>Expense Transactions</h2>
          <p className="section-desc">Manage, edit, or filter your daily transactions</p>
        </div>
      </div>

      {/* Controls Bar: Search, Category Filters, Sort */}
      <div className="controls-bar">
        {/* Search Input */}
        <div className="search-box">
          <span className="search-icon">🔍</span>
          <input
            id="search-input"
            type="text"
            placeholder="Search by title, category, or notes..."
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
          />
          {searchTerm && (
            <button className="clear-search-btn" onClick={() => onSearchChange("")}>
              ✕
            </button>
          )}
        </div>

        {/* Sort Dropdown */}
        <div className="sort-box">
          <label htmlFor="sort-select">Sort by:</label>
          <select
            id="sort-select"
            value={sortBy}
            onChange={(e) => onSortChange(e.target.value)}
          >
            <option value="id-desc">Newest Added</option>
            <option value="id-asc">Oldest Added</option>
            <option value="date-desc">Date (Recent First)</option>
            <option value="date-asc">Date (Oldest First)</option>
            <option value="amount-desc">Amount (High to Low)</option>
            <option value="amount-asc">Amount (Low to High)</option>
          </select>
        </div>
      </div>

      {/* Category Filter Chips */}
      <div className="category-chips-row">
        {categories.map((cat) => (
          <button
            key={cat}
            className={`chip-btn ${selectedCategory === cat ? "active" : ""}`}
            onClick={() => onSelectCategory(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Expenses Table */}
      <div className="table-wrapper">
        {loading ? (
          <div className="loader-box">
            <div className="spinner"></div>
            <p>Loading transactions...</p>
          </div>
        ) : filteredExpenses.length === 0 ? (
          <div className="empty-state">
            <span className="empty-icon">📂</span>
            <h3>No expenses found</h3>
            <p>
              {searchTerm || selectedCategory !== "All"
                ? "Try adjusting your search or category filter."
                : "Click '+ Add Expense' above to record your first transaction!"}
            </p>
          </div>
        ) : (
          <table className="expenses-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Date</th>
                <th>Category</th>
                <th>Title / Notes</th>
                <th className="text-right">Amount</th>
                <th className="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredExpenses.map((exp) => {
                const badge = CATEGORY_COLORS[exp.category] || {
                  bg: "rgba(156, 163, 175, 0.15)",
                  text: "#9ca3af",
                  icon: "🏷️",
                };

                return (
                  <tr key={exp.id} className="expense-row">
                    <td className="exp-id">#{exp.id}</td>
                    <td className="exp-date">
                      <span className="date-badge">{exp.date}</span>
                    </td>
                    <td>
                      <span
                        className="cat-badge"
                        style={{ backgroundColor: badge.bg, color: badge.text }}
                      >
                        {badge.icon} {exp.category}
                      </span>
                    </td>
                    <td className="exp-details">
                      <div className="exp-title">{exp.title}</div>
                      {exp.notes && <div className="exp-notes">{exp.notes}</div>}
                    </td>
                    <td className="exp-amount text-right">
                      ₹{parseFloat(exp.amount).toLocaleString("en-IN", { minimumFractionDigits: 2 })}
                    </td>
                    <td className="text-center">
                      <div className="action-buttons">
                        <button
                          className="action-btn edit-btn"
                          title="Edit Expense"
                          onClick={() => onEdit(exp)}
                        >
                          ✏️
                        </button>
                        <button
                          className="action-btn delete-btn"
                          title="Delete Expense"
                          onClick={() => onDelete(exp.id)}
                        >
                          🗑️
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
