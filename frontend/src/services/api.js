/**
 * API Service for connecting to the FastAPI backend.
 * Base URL: http://127.0.0.1:8000
 */
const BASE_URL = "http://127.0.0.1:8000";

export const api = {
  // Get all expenses with optional filters
  async getExpenses({ category, date, sortBy = "id", order = "desc" } = {}) {
    const params = new URLSearchParams();
    if (category && category !== "All") params.append("category", category);
    if (date) params.append("date", date);
    if (sortBy) params.append("sort_by", sortBy);
    if (order) params.append("order", order);

    const res = await fetch(`${BASE_URL}/expenses?${params.toString()}`);
    if (!res.ok) throw new Error("Failed to fetch expenses");
    return res.json();
  },

  // Add a new expense
  async createExpense(expenseData) {
    const res = await fetch(`${BASE_URL}/expenses`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(expenseData),
    });
    const data = await res.json();
    if (!res.ok) {
      const msg = Array.isArray(data.detail) ? data.detail.join(", ") : (data.detail || "Error adding expense");
      throw new Error(msg);
    }
    return data;
  },

  // Update an existing expense
  async updateExpense(id, updateData) {
    const res = await fetch(`${BASE_URL}/expenses/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updateData),
    });
    const data = await res.json();
    if (!res.ok) {
      const msg = Array.isArray(data.detail) ? data.detail.join(", ") : (data.detail || "Error updating expense");
      throw new Error(msg);
    }
    return data;
  },

  // Delete an expense
  async deleteExpense(id) {
    const res = await fetch(`${BASE_URL}/expenses/${id}`, {
      method: "DELETE",
    });
    if (!res.ok) throw new Error("Failed to delete expense");
    return res.json();
  },

  // Monthly summary report
  async getMonthlyReport() {
    const res = await fetch(`${BASE_URL}/reports/monthly`);
    if (!res.ok) throw new Error("Failed to fetch monthly report");
    return res.json();
  },

  // Category summary report
  async getCategoryReport() {
    const res = await fetch(`${BASE_URL}/reports/category`);
    if (!res.ok) throw new Error("Failed to fetch category report");
    return res.json();
  },

  // Overall statistics report
  async getStatistics() {
    const res = await fetch(`${BASE_URL}/reports/statistics`);
    if (!res.ok) throw new Error("Failed to fetch statistics");
    return res.json();
  },

  // Export CSV URL
  getExportUrl() {
    return `${BASE_URL}/reports/export`;
  },
};
