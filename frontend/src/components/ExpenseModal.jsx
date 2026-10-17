import React, { useState, useEffect } from "react";

const PRESET_CATEGORIES = [
  "Food",
  "Travel",
  "Shopping",
  "Bills",
  "Health",
  "Education",
  "Entertainment",
  "General",
];

export default function ExpenseModal({ isOpen, onClose, onSave, editingExpense }) {
  const [title, setTitle] = useState("");
  const [amount, setAmount] = useState("");
  const [category, setCategory] = useState("Food");
  const [date, setDate] = useState("");
  const [notes, setNotes] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  // Today's date in YYYY-MM-DD format
  const getTodayDate = () => new Date().toISOString().split("T")[0];

  useEffect(() => {
    if (editingExpense) {
      setTitle(editingExpense.title || "");
      setAmount(editingExpense.amount || "");
      setCategory(editingExpense.category || "Food");
      setDate(editingExpense.date || getTodayDate());
      setNotes(editingExpense.notes || "");
    } else {
      setTitle("");
      setAmount("");
      setCategory("Food");
      setDate(getTodayDate());
      setNotes("");
    }
    setError("");
  }, [editingExpense, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!title.trim()) {
      setError("Please enter a title for the expense.");
      return;
    }

    const numAmount = parseFloat(amount);
    if (isNaN(numAmount) || numAmount <= 0) {
      setError("Amount must be a positive number greater than 0.");
      return;
    }

    if (!date) {
      setError("Please select a valid date (YYYY-MM-DD).");
      return;
    }

    setSubmitting(true);
    try {
      await onSave({
        title: title.trim(),
        amount: numAmount,
        category: category.trim(),
        date: date,
        notes: notes.trim(),
      });
      onClose();
    } catch (err) {
      setError(err.message || "Failed to save expense");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-container" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>{editingExpense ? "✏️ Edit Expense" : "➕ Add New Expense"}</h3>
          <button className="close-btn" onClick={onClose} title="Close">
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} className="modal-form">
          {error && <div className="form-error-banner">⚠️ {error}</div>}

          {/* Title */}
          <div className="form-group">
            <label htmlFor="expense-title">Expense Title *</label>
            <input
              id="expense-title"
              type="text"
              placeholder="e.g. Lunch at Cafe, Train Ticket, Groceries"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              autoFocus
            />
          </div>

          {/* Amount & Date in 2 columns */}
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="expense-amount">Amount (₹) *</label>
              <input
                id="expense-amount"
                type="number"
                step="any"
                min="0.01"
                placeholder="0.00"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="expense-date">Date *</label>
              <input
                id="expense-date"
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                required
              />
            </div>
          </div>

          {/* Category Chips / Selector */}
          <div className="form-group">
            <label>Category *</label>
            <div className="category-select-grid">
              {PRESET_CATEGORIES.map((cat) => (
                <button
                  type="button"
                  key={cat}
                  className={`cat-select-btn ${category === cat ? "selected" : ""}`}
                  onClick={() => setCategory(cat)}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>

          {/* Notes */}
          <div className="form-group">
            <label htmlFor="expense-notes">Notes / Remarks (Optional)</label>
            <textarea
              id="expense-notes"
              rows="2"
              placeholder="e.g. Paid via UPI, with office colleagues..."
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
            />
          </div>

          {/* Form Actions */}
          <div className="modal-footer">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onClose}
              disabled={submitting}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={submitting}
            >
              {submitting ? "Saving..." : editingExpense ? "Update Expense" : "Save Expense"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
