#!/usr/bin/env python3
"""
Personal Finance Manager - Main Application
Entry point for the Personal Finance Manager application
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from expense_manager import ExpenseManager
from utils import print_header, print_info

def display_main_menu():
    """Display main menu and handle user choice"""
    expense_manager = ExpenseManager()
    
    while True:
        # Clear screen (for better UX)
        print("\n" * 50)
        
        print_header("PERSONAL FINANCE MANAGER")
        print(f"\n📅 Current Month: {expense_manager.report_generator.get_monthly_report()['month_name']}")
        print(f"💰 Total Expenses: ₹{expense_manager.get_total_expenses():,.2f}")
        print(f"📊 Expenses Count: {len(expense_manager.expenses)}")
        
        print("\n" + "=" * 40)
        print("📋 MAIN MENU")
        print("=" * 40)
        
        print("1. 📝 Add New Expense")
        print("2. 👁️  View All Expenses")
        print("3. 📊 Category Summary")
        print("4. 📈 Monthly Report")
        print("5. 🔍 Search Expenses")
        print("6. 💾 Backup Data")
        print("7. 📤 Export Report")
        print("8. 🛠️  Utilities")
        print("9. ℹ️  Help & Information")
        print("0. 🚪 Exit")
        print("-" * 40)
        
        try:
            choice = input("\nEnter your choice (0-9): ").strip()
            
            if choice == "1":
                add_expense_menu(expense_manager)
            elif choice == "2":
                view_expenses_menu(expense_manager)
            elif choice == "3":
                category_summary_menu(expense_manager)
            elif choice == "4":
                monthly_report_menu(expense_manager)
            elif choice == "5":
                search_expenses_menu(expense_manager)
            elif choice == "6":
                backup_data_menu(expense_manager)
            elif choice == "7":
                export_report_menu(expense_manager)
            elif choice == "8":
                utilities_menu(expense_manager)
            elif choice == "9":
                help_menu()
            elif choice == "0":
                print_info("Thank you for using Personal Finance Manager!")
                expense_manager.save_expenses()
                break
            else:
                print("❌ Invalid choice! Please enter 0-9")
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Application interrupted. Saving data...")
            expense_manager.save_expenses()
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")

def add_expense_menu(expense_manager):
    """Menu for adding new expense"""
    print("\n" + "=" * 40)
    print("📝 ADD NEW EXPENSE")
    print("=" * 40)
    
    try:
        # Get amount
        while True:
            amount_input = input("\nEnter amount (₹): ").strip()
            try:
                amount = float(amount_input)
                if amount <= 0:
                    print("❌ Amount must be greater than 0")
                    continue
                break
            except ValueError:
                print("❌ Please enter a valid number")
        
        # Get category
        print(f"\nAvailable categories: {', '.join(Expense.CATEGORIES)}")
        while True:
            category = input("Enter category: ").strip().title()
            if category in Expense.CATEGORIES:
                break
            else:
                print(f"❌ Category must be one of: {', '.join(Expense.CATEGORIES)}")
        
        # Get date (default to today)
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        date_input = input(f"\nEnter date (YYYY-MM-DD) [Press Enter for today '{today}']: ").strip()
        
        if not date_input:
            date_input = today
        
        # Validate date
        while True:
            try:
                datetime.strptime(date_input, "%Y-%m-%d")
                break
            except ValueError:
                print("❌ Date must be in YYYY-MM-DD format")
                date_input = input("Enter date (YYYY-MM-DD): ").strip()
        
        # Get description
        description = input("\nEnter description (optional): ").strip()
        
        # Create and add expense
        expense = Expense(amount, category, date_input, description)
        
        if expense_manager.add_expense(expense):
            print(f"\n✅ Expense added successfully!")
            print(f"   Amount: ₹{amount:,.2f}")
            print(f"   Category: {category}")
            print(f"   Date: {date_input}")
            if description:
                print(f"   Description: {description}")
        else:
            print("❌ Failed to add expense!")
            
    except KeyboardInterrupt:
        print("\n⚠️  Cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input("\nPress Enter to continue...")

def view_expenses_menu(expense_manager):
    """Menu for viewing all expenses"""
    print("\n" + "=" * 40)
    print("👁️  ALL EXPENSES")
    print("=" * 40)
    
    if not expense_manager.expenses:
        print("\n📭 No expenses found!")
        input("\nPress Enter to continue...")
        return
    
    print(f"\nTotal Expenses: {len(expense_manager.expenses)}")
    print("-" * 80)
    print(f"{'Date':12} {'Category':15} {'Amount':15} {'Description':30}")
    print("-" * 80)
    
    total = 0
    for expense in expense_manager.expenses:
        date_str = expense.date
        if len(expense.description) > 30:
            desc = expense.description[:27] + "..."
        else:
            desc = expense.description
        
        print(f"{date_str:12} {expense.category:15} ₹{expense.amount:13,.2f} {desc:30}")
        total += expense.amount
    
    print("-" * 80)
    print(f"{'TOTAL':27} ₹{total:13,.2f}")
    
    input("\nPress Enter to continue...")

def category_summary_menu(expense_manager):
    """Menu for category summary"""
    print("\n" + "=" * 40)
    print("📊 CATEGORY SUMMARY")
    print("=" * 40)
    
    if not expense_manager.expenses:
        print("\n📭 No expenses found!")
        input("\nPress Enter to continue...")
        return
    
    report = expense_manager.get_category_summary()
    
    print(f"\nTotal Expenses: ₹{report['total']:,.2f}")
    print(f"Number of Expenses: {report['count']}")
    print("-" * 60)
    
    print("\nCategory Breakdown:")
    print("-" * 60)
    
    for item in report["summary"]:
        percentage = item['percentage']
        bar_length = int(percentage / 2)  # Scale for display
        bar = "█" * bar_length
        print(f"{item['category']:20}: ₹{item['amount']:10,.2f} ({percentage:5.1f}%) {bar}")
    
    print("-" * 60)
    
    input("\nPress Enter to continue...")

def monthly_report_menu(expense_manager):
    """Menu for monthly report"""
    print("\n" + "=" * 40)
    print("📈 MONTHLY REPORT")
    print("=" * 40)
    
    if not expense_manager.expenses:
        print("\n📭 No expenses found!")
        input("\nPress Enter to continue...")
        return
    
    from utils import get_current_month
    current_month = get_current_month()
    
    month_input = input(f"\nEnter month (YYYY-MM) [Press Enter for '{current_month}']: ").strip()
    if not month_input:
        month_input = current_month
    
    try:
        from datetime import datetime
        datetime.strptime(f"{month_input}-01", "%Y-%m-%d")
    except ValueError:
        print(f"❌ Invalid month format! Using '{current_month}'")
        month_input = current_month
    
    report = expense_manager.get_monthly_report(month_input)
    
    print(f"\n📅 Monthly Report: {report['month_name']}")
    print("-" * 60)
    print(f"Total Expenses: ₹{report['total_expenses']:,.2f}")
    print(f"Number of Expenses: {report['expense_count']}")
    print(f"Average per Day: ₹{report['avg_per_day']:,.2f}")
    print("-" * 60)
    
    if report['category_totals']:
        print("\nCategory Breakdown:")
        print("-" * 60)
        for category, amount in report['category_totals'].items():
            percentage = (amount / report['total_expenses'] * 100) if report['total_expenses'] > 0 else 0
            print(f"{category:20}: ₹{amount:10,.2f} ({percentage:5.1f}%)")
    
    if report['top_expenses']:
        print("\nTop 5 Expenses:")
        print("-" * 60)
        for expense in report['top_expenses']:
            print(f"  ₹{expense.amount:8,.2f} - {expense.category:15} - {expense.description}")
    
    input("\nPress Enter to continue...")

def search_expenses_menu(expense_manager):
    """Menu for searching expenses"""
    print("\n" + "=" * 40)
    print("🔍 SEARCH EXPENSES")
    print("=" * 40)
    
    if not expense_manager.expenses:
        print("\n📭 No expenses found!")
        input("\nPress Enter to continue...")
        return
    
    print("\nSearch by:")
    print("1. Category")
    print("2. Date")
    print("3. Description")
    print("-" * 40)
    
    choice = input("Enter choice (1-3): ").strip()
    
    results = []
    
    if choice == "1":
        print(f"\nAvailable categories: {', '.join(Expense.CATEGORIES)}")
        category = input("Enter category to search: ").strip().title()
        results = expense_manager.search_expenses(category, "category")
    
    elif choice == "2":
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        results = expense_manager.search_expenses(date_str, "date")
    
    elif choice == "3":
        keyword = input("Enter keyword to search in description: ").strip().lower()
        results = expense_manager.search_expenses(keyword, "description")
    
    else:
        print("❌ Invalid choice!")
        input("\nPress Enter to continue...")
        return
    
    # Display results
    print("\n" + "=" * 40)
    print(f"📋 SEARCH RESULTS ({len(results)} found)")
    print("=" * 40)
    
    if not results:
        print("\n🔍 No matching expenses found!")
    else:
        total = 0
        for expense in results:
            print(f"\n  Date: {expense.date}")
            print(f"  Category: {expense.category}")
            print(f"  Amount: ₹{expense.amount:,.2f}")
            if expense.description:
                print(f"  Description: {expense.description}")
            print("-" * 40)
            total += expense.amount
        
        print(f"\n💰 Total of matching expenses: ₹{total:,.2f}")
    
    input("\nPress Enter to continue...")

def backup_data_menu(expense_manager):
    """Menu for backup operations"""
    print("\n" + "=" * 40)
    print("💾 BACKUP DATA")
    print("=" * 40)
    
    print("\n1. Create Backup Now")
    print("2. List Existing Backups")
    print("-" * 40)
    
    choice = input("Enter choice (1-2): ").strip()
    
    if choice == "1":
        backup_file = expense_manager.file_manager.create_backup()
        if backup_file:
            import os
            print(f"\n✅ Backup created: {os.path.basename(backup_file)}")
        else:
            print("\n❌ Failed to create backup!")
    
    elif choice == "2":
        backups = expense_manager.file_manager.list_backups()
        
        if not backups:
            print("\n📭 No backups found!")
        else:
            print(f"\nFound {len(backups)} backup(s):")
            print("-" * 40)
            for backup in backups:
                size_kb = backup['size'] / 1024
                print(f"  • {backup['filename']} ({size_kb:.1f} KB)")
    
    else:
        print("❌ Invalid choice!")
    
    input("\nPress Enter to continue...")

def export_report_menu(expense_manager):
    """Menu for exporting reports"""
    print("\n" + "=" * 40)
    print("📤 EXPORT REPORT")
    print("=" * 40)
    
    if not expense_manager.expenses:
        print("\n📭 No expenses found to export!")
        input("\nPress Enter to continue...")
        return
    
    print("\nExport Options:")
    print("1. Category Summary Report")
    print("2. Monthly Report")
    print("-" * 40)
    
    choice = input("Enter choice (1-2): ").strip()
    
    if choice == "1":
        report_data = expense_manager.get_category_summary()
        filename = expense_manager.export_report(report_data, "category")
    
    elif choice == "2":
        from utils import get_current_month
        current_month = get_current_month()
        month_input = input(f"Enter month (YYYY-MM) [Press Enter for '{current_month}']: ").strip()
        
        if not month_input:
            month_input = current_month
        
        report_data = expense_manager.get_monthly_report(month_input)
        filename = expense_manager.export_report(report_data, "monthly")
    
    else:
        print("❌ Invalid choice!")
        input("\nPress Enter to continue...")
        return
    
    if filename:
        print(f"\n✅ Report exported to: {filename}")
    else:
        print("\n❌ Failed to export report!")
    
    input("\nPress Enter to continue...")

def utilities_menu(expense_manager):
    """Utilities menu"""
    print("\n" + "=" * 40)
    print("🛠️  UTILITIES")
    print("=" * 40)
    
    print("\n1. Clear All Expenses")
    print("2. Generate Sample Data")
    print("3. View Statistics")
    print("-" * 40)
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        confirm = input("\n⚠️  WARNING: This will delete ALL expenses! Type 'DELETE' to confirm: ")
        if confirm == "DELETE":
            expense_manager.clear_all_expenses()
            print("✅ All expenses cleared!")
        else:
            print("❌ Operation cancelled.")
    
    elif choice == "2":
        count_input = input("\nHow many sample expenses to generate? (default: 10): ").strip()
        try:
            count = int(count_input) if count_input else 10
            expense_manager.generate_sample_data(count)
            print(f"✅ Generated {count} sample expenses!")
        except ValueError:
            print("❌ Invalid number!")
    
    elif choice == "3":
        stats = expense_manager.get_statistics()
        
        if not stats:
            print("\n📭 No statistics available!")
        else:
            print("\n📊 STATISTICS")
            print("-" * 40)
            print(f"Total Expenses: ₹{stats['total']:,.2f}")
            print(f"Number of Expenses: {stats['count']}")
            print(f"Average Expense: ₹{stats['average']:,.2f}")
            print(f"Highest Expense: ₹{stats['max']:,.2f}")
            print(f"Lowest Expense: ₹{stats['min']:,.2f}")
            print(f"Date Range: {stats['start_date']} to {stats['end_date']}")
    
    else:
        print("❌ Invalid choice!")
    
    input("\nPress Enter to continue...")

def help_menu():
    """Display help information"""
    print("\n" + "=" * 60)
    print("ℹ️  HELP & INFORMATION")
    print("=" * 60)
    
    print("\n📖 PERSONAL FINANCE MANAGER - USER GUIDE")
    print("-" * 60)
    
    print("\n1. ADDING EXPENSES:")
    print("   • Use option 1 from main menu")
    print("   • Enter amount, category, date, and description")
    print("   • Date format: YYYY-MM-DD (e.g., 2024-01-15)")
    
    print("\n2. VIEWING EXPENSES:")
    print("   • Option 2: View all expenses")
    print("   • Option 3: Category-wise summary")
    print("   • Option 4: Monthly detailed report")
    
    print("\n3. SEARCHING EXPENSES:")
    print("   • Option 5: Search by category, date, or description")
    
    print("\n4. DATA MANAGEMENT:")
    print("   • Option 6: Backup and restore data")
    print("   • Option 7: Export reports to files")
    print("   • Option 8: Utilities and maintenance")
    
    print("\n5. TIPS:")
    print("   • Regular backups prevent data loss")
    print("   • Use consistent category names")
    print("   • Export monthly reports for record keeping")
    
    print("\n" + "=" * 60)
    input("\nPress Enter to return to main menu...")

def main():
    """Main application entry point"""
    try:
        # Display welcome message
        print_header("PERSONAL FINANCE MANAGER")
        print("\nWelcome to your personal finance tracking system!")
        print("Managing your expenses has never been easier.")
        
        # Start main menu
        display_main_menu()
        
        # Save before exiting
        print("\n✅ Application closed. Data saved successfully.")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Application interrupted by user")
        print("Data saved. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your setup and try again.")

if __name__ == "__main__":
    main()