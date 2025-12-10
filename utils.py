"""
Utility Functions Module
Helper functions for validation, formatting, etc.
"""

import re
from datetime import datetime, timedelta

def validate_date(date_str):
    """
    Validate date string format YYYY-MM-DD
    
    Args:
        date_str (str): Date string to validate
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not date_str:
        return False, "Date cannot be empty"
    
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        
        # Check if date is not in the future
        input_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.now().date()
        
        if input_date > today:
            return False, "Date cannot be in the future"
        
        return True, ""
        
    except ValueError:
        return False, "Date must be in YYYY-MM-DD format"

def validate_amount(amount_str):
    """
    Validate amount string
    
    Args:
        amount_str (str): Amount string to validate
    
    Returns:
        tuple: (is_valid, error_message, amount_float)
    """
    if not amount_str:
        return False, "Amount cannot be empty", 0
    
    try:
        amount = float(amount_str)
        
        if amount <= 0:
            return False, "Amount must be greater than 0", 0
        
        if amount > 10000000:  # 10 million limit
            return False, "Amount is too large", 0
        
        return True, "", round(amount, 2)
        
    except ValueError:
        return False, "Amount must be a valid number", 0

def validate_category(category, valid_categories):
    """
    Validate category
    
    Args:
        category (str): Category to validate
        valid_categories (list): List of valid categories
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not category:
        return False, "Category cannot be empty"
    
    category_lower = category.strip().title()
    
    if category_lower not in valid_categories:
        valid_str = ", ".join(valid_categories)
        return False, f"Category must be one of: {valid_str}"
    
    return True, ""

def format_currency(amount):
    """
    Format amount as Indian Rupees
    
    Args:
        amount (float): Amount to format
    
    Returns:
        str: Formatted currency string
    """
    return f"₹{amount:,.2f}"

def format_date(date_str):
    """
    Format date string to more readable format
    
    Args:
        date_str (str): Date in YYYY-MM-DD format
    
    Returns:
        str: Formatted date string
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d %b %Y")
    except:
        return date_str

def get_current_month():
    """Get current month in YYYY-MM format"""
    return datetime.now().strftime("%Y-%m")

def get_month_name(month_str):
    """Convert YYYY-MM to month name"""
    try:
        date_obj = datetime.strptime(f"{month_str}-01", "%Y-%m-%d")
        return date_obj.strftime("%B %Y")
    except:
        return month_str

def clear_screen():
    """Clear terminal screen"""
    print("\n" * 50)

def print_header(title):
    """Print formatted header"""
    print("=" * 50)
    print(f"{title:^50}")
    print("=" * 50)

def print_success(message):
    """Print success message in green"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message in red"""
    print(f"❌ {message}")

def print_warning(message):
    """Print warning message in yellow"""
    print(f"⚠️  {message}")

def print_info(message):
    """Print info message in blue"""
    print(f"ℹ️  {message}")