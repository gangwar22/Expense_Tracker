import React from "react";

const CATEGORY_ICONS = {
  Food: "🍔",
  Travel: "🚗",
  Shopping: "🛍️",
  Bills: "💡",
  Health: "💊",
  Education: "📚",
  Entertainment: "🎬",
  General: "📦",
};

export default function CategoryReport({ categories, monthly, totalAmount }) {
  const categoryEntries = Object.entries(categories || {});
  const monthlyEntries = Object.entries(monthly || {});

  return (
    <div className="reports-section-grid">
      {/* Category Breakdown Card */}
      <div className="report-card">
        <div className="report-card-header">
          <h3>Category Breakdown</h3>
          <span className="badge">{categoryEntries.length} Categories</span>
        </div>

        {categoryEntries.length === 0 ? (
          <p className="empty-text">No category data available yet.</p>
        ) : (
          <div className="category-list">
            {categoryEntries.map(([cat, amount]) => {
              const percentage = totalAmount > 0 ? Math.round((amount / totalAmount) * 100) : 0;
              const icon = CATEGORY_ICONS[cat] || "🏷️";
              return (
                <div key={cat} className="category-item">
                  <div className="category-header">
                    <span className="category-name">
                      <span className="cat-icon">{icon}</span> {cat}
                    </span>
                    <span className="category-amount">
                      ₹{amount.toLocaleString("en-IN")} <span className="cat-pct">({percentage}%)</span>
                    </span>
                  </div>
                  <div className="progress-bar-bg">
                    <div
                      className="progress-bar-fill"
                      style={{ width: `${Math.min(percentage, 100)}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Monthly Breakdown Card */}
      <div className="report-card">
        <div className="report-card-header">
          <h3>Monthly Spending</h3>
          <span className="badge">{monthlyEntries.length} Months</span>
        </div>

        {monthlyEntries.length === 0 ? (
          <p className="empty-text">No monthly data available yet.</p>
        ) : (
          <div className="monthly-grid">
            {monthlyEntries.map(([month, amount]) => (
              <div key={month} className="monthly-pill-card">
                <span className="month-name">📅 {month}</span>
                <span className="month-amount">₹{amount.toLocaleString("en-IN")}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
