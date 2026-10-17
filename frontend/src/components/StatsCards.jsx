import React from "react";

export default function StatsCards({ stats }) {
  const cards = [
    {
      id: "stat-total",
      label: "Total Expenses",
      value: `₹${(stats.total || 0).toLocaleString("en-IN", { minimumFractionDigits: 2 })}`,
      icon: "💳",
      gradient: "linear-gradient(135deg, #6366f1 0%, #4338ca 100%)",
      glowColor: "rgba(99, 102, 241, 0.25)",
    },
    {
      id: "stat-average",
      label: "Average Expense",
      value: `₹${(stats.average || 0).toLocaleString("en-IN", { minimumFractionDigits: 2 })}`,
      icon: "📊",
      gradient: "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)",
      glowColor: "rgba(6, 182, 212, 0.25)",
    },
    {
      id: "stat-highest",
      label: "Highest Expense",
      value: `₹${(stats.highest || 0).toLocaleString("en-IN", { minimumFractionDigits: 2 })}`,
      icon: "🔥",
      gradient: "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
      glowColor: "rgba(245, 158, 11, 0.25)",
    },
    {
      id: "stat-count",
      label: "Total Entries",
      value: stats.count || 0,
      icon: "📝",
      gradient: "linear-gradient(135deg, #10b981 0%, #059669 100%)",
      glowColor: "rgba(16, 185, 129, 0.25)",
    },
  ];

  return (
    <div className="stats-grid">
      {cards.map((c) => (
        <div
          key={c.id}
          id={c.id}
          className="stat-card"
          style={{ "--glow-color": c.glowColor }}
        >
          <div className="stat-card-header">
            <span className="stat-label">{c.label}</span>
            <div className="stat-icon-wrapper" style={{ background: c.gradient }}>
              {c.icon}
            </div>
          </div>
          <div className="stat-value">{c.value}</div>
        </div>
      ))}
    </div>
  );
}
