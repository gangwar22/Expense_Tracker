"""
Analytics & Reports Module
Uses Pandas and NumPy to analyze expenses data.
Har function bohot simple hai taaki aap viva/interview me aaram se explain kar sakein.
"""
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

from app.config import CSV_FILE_PATH, CSV_HEADERS
from app.utils import ensure_csv_file


class ExpenseAnalytics:
    """
    Pandas aur NumPy ka use karke expenses ka data analyze karne wali class.
    """

    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = file_path or CSV_FILE_PATH

    def _get_dataframe(self) -> pd.DataFrame:
        """
        1. CSV file exist karti hai ya nahi ensure karta hai.
        2. pd.read_csv() se CSV ko ek Pandas Table (DataFrame) me load karta hai.
        3. 'date' column ko datetime me aur 'amount' ko numbers me convert karta hai.
        """
        ensure_csv_file(self.file_path)
        try:
            df = pd.read_csv(self.file_path)
        except Exception:
            return pd.DataFrame(columns=CSV_HEADERS)

        # Agar table khali hai toh empty DataFrame return karo
        if df.empty or "amount" not in df.columns:
            return pd.DataFrame(columns=CSV_HEADERS)

        # Types safely set karna: amount -> float, date -> datetime
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["category"] = df["category"].fillna("General").astype(str).str.title()

        # Jin rows me valid date hai sirf unko rakhein
        df = df.dropna(subset=["date"])
        return df

    def get_monthly_summary(self) -> Dict[str, float]:
        """
        PANDAS FEATURE:
        Har Month ka total kharcha nikalta hai (Jaise: {'September': 4200.0}).
        """
        df = self._get_dataframe()
        if df.empty:
            return {}

        # Date se Month ka naam nikalna (jaise '2026-09-25' -> 'September')
        df["month"] = df["date"].dt.strftime("%B")

        # Pandas groupby: Month ke hisaab se amount ka sum karna
        monthly_totals = df.groupby("month", sort=False)["amount"].sum()

        # Dictionary me convert karke return karna
        return {month: round(float(total), 2) for month, total in monthly_totals.items()}

    def get_category_summary(self) -> Dict[str, float]:
        """
        PANDAS FEATURE:
        Category ke hisaab se total spending nikalta hai (Jaise: {'Food': 1200.0, 'Travel': 600.0}).
        """
        df = self._get_dataframe()
        if df.empty:
            return {}

        # Category column par groupby karke sum nikalna
        category_totals = df.groupby("category")["amount"].sum()
        return {category: round(float(total), 2) for category, total in category_totals.items()}

    def get_overall_statistics(self) -> Dict[str, Any]:
        """
        NUMPY FEATURE:
        NumPy ke fast functions use karke overall statistics calculate karna:
        - np.sum()  -> Total expenses
        - np.mean() -> Average expense
        - np.max()  -> Sabse bada expense (Highest)
        - np.min()  -> Sabse chhota expense (Lowest)
        - len()     -> Total number of expenses (Count)
        """
        df = self._get_dataframe()
        if df.empty:
            return {
                "total": 0.0,
                "average": 0.0,
                "highest": 0.0,
                "count": 0,
                "lowest": 0.0,
            }

        # DataFrame column ko NumPy array me convert karna
        amounts = df["amount"].to_numpy()

        # NumPy functions se calculate karna
        total = float(np.sum(amounts))
        average = float(np.mean(amounts))
        highest = float(np.max(amounts))
        lowest = float(np.min(amounts))
        count = int(len(amounts))

        return {
            "total": round(total, 2),
            "average": round(average, 2),
            "highest": round(highest, 2),
            "count": count,
            "lowest": round(lowest, 2),
        }


# Global object jise main.py me use karenge
expense_analytics = ExpenseAnalytics()
