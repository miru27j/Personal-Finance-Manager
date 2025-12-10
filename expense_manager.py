"""
Expense Manager Module
Main controller that ties all components together
"""

from file_manager import FileManager
from reports import ReportGenerator
from expense import Expense
from utils import get_current_month
import random
from datetime import datetime, timedelta

class ExpenseManager:
    """Main controller class for expense management"""
    
    def __init__(self):
        """Initialize expense manager"""
        self.file_manager = FileManager()
        self.expenses = []
        self.report_generator = None
        self.load_expenses()
    
    def load_expenses(self):
        """Load expenses from file"""
        self.expenses = self.file_manager.load_expenses()
        self.report_generator = ReportGenerator(self.expenses)
    
    def save_expenses(self):
        """Save expenses to file"""
        return self.file_manager.save_expenses(self.expenses)
    
    def add_expense(self, expense):
        """
        Add a new expense
        
        Args:
            expense (Expense): Expense object to add
        
        Returns:
            bool: True if successful
        """
        try:
            self.expenses.append(expense)
            self.report_generator = ReportGenerator(self.expenses)
            success = self.save_expenses()
            return success
        except Exception as e:
            print(f"Error adding expense: {e}")
            return False
    
    def get_total_expenses(self):
        """Get total of all expenses"""
        return sum(expense.amount for expense in self.expenses)
    
    def get_monthly_expenses(self, month=None):
        """
        Get expenses for a specific month
        
        Args:
            month (str): Month in YYYY-MM format
        
        Returns:
            list: Expenses for the month
        """
        if not month:
            month = get_current_month()
        
        return [
            exp for exp in self.expenses 
            if exp.date.startswith(month)
        ]
    
    def get_category_summary(self):
        """Get category-wise expense summary"""
        return self.report_generator.get_category_summary()
    
    def get_monthly_report(self, month=None):
        """Get monthly expense report"""
        return self.report_generator.get_monthly_report(month)
    
    def search_expenses(self, search_term, search_by="all"):
        """Search expenses by criteria"""
        return self.report_generator.search_expenses(search_term, search_by)
    
    def export_report(self, report_data, report_type):
        """Export report to file"""
        return self.report_generator.export_report(report_data, report_type)
    
    def clear_all_expenses(self):
        """Clear all expenses"""
        self.expenses = []
        self.report_generator = ReportGenerator(self.expenses)
        self.save_expenses()
    
    def generate_sample_data(self, count=10):
        """Generate sample expense data for testing"""
        categories = Expense.CATEGORIES
        descriptions = [
            "Groceries", "Restaurant dinner", "Petrol", "Bus fare", 
            "Movie tickets", "Online shopping", "Electricity bill", 
            "Doctor visit", "Books", "Coffee", "Lunch", "Snacks",
            "Taxi", "Parking", "Netflix subscription", "Gym membership"
        ]
        
        # Clear existing data first
        self.expenses = []
        
        # Generate sample expenses
        start_date = datetime.now() - timedelta(days=30)
        
        for i in range(count):
            amount = round(random.uniform(50, 5000), 2)
            category = random.choice(categories)
            date = (start_date + timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
            description = random.choice(descriptions)
            
            expense = Expense(amount, category, date, description)
            self.expenses.append(expense)
        
        self.report_generator = ReportGenerator(self.expenses)
        self.save_expenses()
    
    def get_statistics(self):
        """Get comprehensive statistics"""
        if not self.expenses:
            return {}
        
        # Basic stats
        amounts = [exp.amount for exp in self.expenses]
        dates = [exp.date for exp in self.expenses]
        
        # Monthly stats
        monthly_stats = {}
        for exp in self.expenses:
            month = exp.date[:7]  # YYYY-MM
            if month not in monthly_stats:
                monthly_stats[month] = {"total": 0, "count": 0}
            monthly_stats[month]["total"] += exp.amount
            monthly_stats[month]["count"] += 1
        
        # Category totals
        category_totals = {}
        for exp in self.expenses:
            category_totals[exp.category] = category_totals.get(exp.category, 0) + exp.amount
        
        return {
            "total": sum(amounts),
            "count": len(amounts),
            "average": sum(amounts) / len(amounts) if amounts else 0,
            "min": min(amounts) if amounts else 0,
            "max": max(amounts) if amounts else 0,
            "start_date": min(dates) if dates else "",
            "end_date": max(dates) if dates else "",
            "monthly_stats": monthly_stats,
            "category_totals": category_totals
        }