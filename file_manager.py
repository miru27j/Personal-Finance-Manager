"""
File Manager Module - FIXED VERSION
Handles CSV file operations for data persistence
"""

import csv
import os
import shutil
from datetime import datetime
from expense import Expense

class FileManager:
    """Manages all file operations for expense data"""
    
    def __init__(self, data_folder="data"):
        """Initialize file manager with data folder"""
        self.data_folder = data_folder
        self.expenses_file = os.path.join(data_folder, "expenses.csv")
        self.backup_folder = os.path.join(data_folder, "backups")
        self._ensure_folders_exist()
    
    def _ensure_folders_exist(self):
        """Create necessary folders if they don't exist - FIXED for Windows"""
        try:
            # Check if 'data' exists and is a file (not a folder)
            if os.path.exists(self.data_folder) and not os.path.isdir(self.data_folder):
                print(f"⚠️  Found a file named '{self.data_folder}' instead of folder.")
                print(f"   Renaming it to '{self.data_folder}_old.txt'")
                
                # Rename the file to avoid conflict
                old_file = f"{self.data_folder}_old.txt"
                os.rename(self.data_folder, old_file)
                print(f"✅ Renamed to: {old_file}")
            
            # Create the directory
            os.makedirs(self.data_folder, exist_ok=True)
            
            # Check if 'backups' exists and is a file
            if os.path.exists(self.backup_folder) and not os.path.isdir(self.backup_folder):
                print(f"⚠️  Found a file named '{self.backup_folder}' instead of folder.")
                print(f"   Renaming it to '{self.backup_folder}_old.txt'")
                
                # Rename the file
                old_backup = f"{self.backup_folder}_old.txt"
                os.rename(self.backup_folder, old_backup)
                print(f"✅ Renamed to: {old_backup}")
            
            # Create the directory
            os.makedirs(self.backup_folder, exist_ok=True)
            
        except Exception as e:
            print(f"❌ Error creating folders: {e}")
            print("   Trying alternative approach...")
            
            # Alternative approach
            if not os.path.exists(self.data_folder):
                os.mkdir(self.data_folder)
            if not os.path.exists(self.backup_folder):
                os.mkdir(self.backup_folder)
    
    def save_expenses(self, expenses):
        """
        Save list of expenses to CSV file
        
        Args:
            expenses (list): List of Expense objects
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create backup before saving
            self.create_backup()
            
            # Prepare data for CSV
            rows = []
            for expense in expenses:
                expense_dict = expense.to_dict()
                rows.append({
                    "Date": expense_dict["date"],
                    "Category": expense_dict["category"],
                    "Amount": expense_dict["amount"],
                    "Description": expense_dict["description"]
                })
            
            # Write to CSV
            with open(self.expenses_file, "w", newline="", encoding="utf-8") as file:
                fieldnames = ["Date", "Category", "Amount", "Description"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving expenses: {e}")
            return False
    
    def load_expenses(self):
        """
        Load expenses from CSV file
        
        Returns:
            list: List of Expense objects
        """
        expenses = []
        
        try:
            # Check if file exists
            if not os.path.exists(self.expenses_file):
                print("ℹ️  No expense data found. Starting fresh.")
                return expenses
            
            # Read from CSV
            with open(self.expenses_file, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        expense = Expense(
                            amount=row["Amount"],
                            category=row["Category"],
                            date=row["Date"],
                            description=row["Description"]
                        )
                        expenses.append(expense)
                    except ValueError as e:
                        print(f"⚠️  Skipping invalid row: {e}")
                        continue
            
            print(f"✅ Loaded {len(expenses)} expenses from file")
            
        except Exception as e:
            print(f"❌ Error loading expenses: {e}")
        
        return expenses
    
    def create_backup(self):
        """Create a backup of the expenses file"""
        try:
            if os.path.exists(self.expenses_file):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = os.path.join(self.backup_folder, f"expenses_backup_{timestamp}.csv")
                shutil.copy2(self.expenses_file, backup_file)
                return backup_file
        except Exception as e:
            print(f"⚠️  Could not create backup: {e}")
        
        return None
    
    def restore_backup(self, backup_file):
        """Restore expenses from a backup file"""
        try:
            if os.path.exists(backup_file):
                shutil.copy2(backup_file, self.expenses_file)
                return True
        except Exception as e:
            print(f"❌ Error restoring backup: {e}")
        
        return False
    
    def list_backups(self):
        """List all available backup files"""
        try:
            backups = []
            for file in os.listdir(self.backup_folder):
                if file.endswith(".csv"):
                    filepath = os.path.join(self.backup_folder, file)
                    backups.append({
                        "filename": file,
                        "path": filepath,
                        "size": os.path.getsize(filepath)
                    })
            
            # Sort by filename (which includes timestamp)
            backups.sort(key=lambda x: x["filename"], reverse=True)
            return backups
            
        except Exception as e:
            print(f"❌ Error listing backups: {e}")
            return []