"""
Expense Class Module
Handles expense creation and management
"""

import datetime

class Expense:
    """Expense class to represent a single expense entry"""
    
    # Valid expense categories
    CATEGORIES = [
        "Food", "Transport", "Entertainment", 
        "Shopping", "Bills", "Healthcare", 
        "Education", "Other"
    ]
    
    def __init__(self, amount, category, date, description=""):
        """
        Initialize a new Expense
        
        Args:
            amount (float): Expense amount (must be positive)
            category (str): Expense category
            date (str): Date in YYYY-MM-DD format
            description (str): Description of expense
        """
        self.amount = self._validate_amount(amount)
        self.category = self._validate_category(category)
        self.date = self._validate_date(date)
        self.description = description.strip()
        self.created_at = datetime.datetime.now()
    
    def _validate_amount(self, amount):
        """Validate and convert amount to float"""
        try:
            amount_float = float(amount)
            if amount_float <= 0:
                raise ValueError("Amount must be greater than 0")
            return round(amount_float, 2)
        except (ValueError, TypeError):
            raise ValueError("Amount must be a valid number")
    
    def _validate_category(self, category):
        """Validate category is in allowed list"""
        if category not in self.CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(self.CATEGORIES)}")
        return category
    
    def _validate_date(self, date_str):
        """Validate date format is YYYY-MM-DD"""
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    
    def to_dict(self):
        """Convert expense to dictionary for CSV storage"""
        return {
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "description": self.description,
            "created_at": self.created_at.isoformat()
        }
    
    def __str__(self):
        """String representation of expense"""
        return f"[{self.date}] {self.category}: ₹{self.amount:.2f} - {self.description}"
    
    def __repr__(self):
        """Detailed representation"""
        return f"Expense(amount={self.amount}, category='{self.category}', date='{self.date}')"