# src/app.py
import sys
import os
from datetime import datetime

# Add root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ✅ FIXED: Use correct import path
from src.core.rag_pipeline import query_rag
from src.hr_specific.employee_db import EmployeeDatabase
from src.hr_specific.leave_manager import LeaveManager
from src.hr_specific.holiday_calendar import HolidayCalendar
from src.hr_specific.hr_utils import format_leave_info, get_personalized_prompt

def print_welcome():
    print("\n" + "="*60)
    print("🚀 HR AGENT - Employee Support System")
    print("="*60)
    print("\n📋 Commands:")
    print("  'balance'   - Check your leave balance")
    print("  'holidays'  - View company holidays")
    print("  'exit'      - Exit the app")
    print("  Or ask any HR question\n")

def login_employee(emp_db):
    """Simple employee login"""
    print("="*60)
    print("👤 LOGIN")
    print("="*60)
    
    employee_id = input("\nEnter your Employee ID (or 'guest' to continue as guest): ").strip()
    
    if employee_id.lower() == 'guest':
        print("\n✅ Running as guest.\n")
        return None
    
    employee = emp_db.get_employee(employee_id)
    
    if not employee:
        print(f"\n❌ Employee ID '{employee_id}' not found in system.")
        print("ℹ️ Available IDs: E001, E002, E003, E004, E005, E010, E011, E012, E013, E015")
        print("\nRetrying...\n")
        return login_employee(emp_db)
    
    print(f"\n✅ Welcome, {employee.name}!")
    print(f"📊 Department: {employee.department}")
    print(f"💼 Designation: {employee.designation}\n")
    
    return employee

def show_leave_balance(employee, leave_mgr):
    """Show employee's leave balance"""
    if not employee:
        print("❌ Please login to check your leave balance.\n")
        return
    
    balance = leave_mgr.check_leave_balance(employee.employee_id)
    print(f"\n📊 Your Leave Balance: {balance} days\n")

def show_holidays(holiday_cal):
    """Show all company holidays"""
    holidays = holiday_cal.get_all_holidays()
    
    print("\n📅 Company Holidays 2026:")
    print("-" * 40)
    for h in holidays:
        date_str = h['date'].strftime('%B %d, %Y')
        print(f"  {date_str:20} : {h['name']}")
    print("-" * 40 + "\n")

def apply_for_leave(employee, leave_mgr):
    """Apply for leave"""
    if not employee:
        print("❌ Please login to apply for leave.\n")
        return
    
    print("\n" + "="*60)
    print("📝 LEAVE APPLICATION FORM")
    print("="*60)
    
    balance = leave_mgr.check_leave_balance(employee.employee_id)
    print(f"\n📊 Available Leave: {balance} days\n")
    
    try:
        from_date_str = input("From date (YYYY-MM-DD): ").strip()
        to_date_str = input("To date (YYYY-MM-DD): ").strip()
        reason = input("Reason: ").strip()
        
        from_date = datetime.strptime(from_date_str, "%Y-%m-%d")
        to_date = datetime.strptime(to_date_str, "%Y-%m-%d")
        
        days_requested = (to_date - from_date).days
        
        print(f"\n📋 Requested: {days_requested} day(s)")
        
        result = leave_mgr.apply_for_leave(
            employee.employee_id,
            "ANNUAL",
            from_date,
            to_date,
            reason
        )
        
        if result['status'] == 'success':
            print(f"✅ {result['message']}")
            print(f"   Request ID: {result['request_id']}")
        else:
            print(f"❌ {result['message']}")
        
        print()
        
    except ValueError as e:
        print(f"\n❌ Invalid input: {e}")
        print("ℹ️ Date format must be YYYY-MM-DD (e.g., 2026-04-15)\n")

def handle_hr_query(query, employee, leave_mgr):
    """Process HR query using RAG agent"""
    print("\n⏳ Processing your query...")
    print("-" * 60)
    
    try:
        # Get RAG answer
        answer = query_rag(query)
        
        print("\n📄 ANSWER:")
        print("-" * 60)
        print(answer)
        print("-" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error processing query: {e}")
        print("ℹ️ Make sure you've run the ingestion script first!\n")

def main():
    """Main application loop"""
    
    # Initialize HR components
    try:
        print("\n⏳ Initializing HR Agent...")
        emp_db = EmployeeDatabase()
        leave_mgr = LeaveManager(emp_db)
        holiday_cal = HolidayCalendar()
        print("✅ All systems ready!\n")
    except Exception as e:
        print(f"❌ Error initializing: {e}")
        print("Make sure all data files exist in data/employee_data/")
        return
    
    # Welcome screen
    print_welcome()
    
    # Login
    employee = login_employee(emp_db)
    
    # Main loop
    while True:
        try:
            query = input("\n🤖 Ask HR: ").strip()
            
            if not query:
                continue
            
            # Check for special commands
            if query.lower() == "exit" or query.lower() == "quit":
                print("\n👋 Thank you for using HR Agent. Goodbye!")
                break
            
            elif query.lower() == "balance":
                show_leave_balance(employee, leave_mgr)
                continue
            
            elif query.lower() == "holidays":
                show_holidays(holiday_cal)
                continue
            
            elif query.lower() == "apply":
                apply_for_leave(employee, leave_mgr)
                continue
            
            # General HR query
            else:
                handle_hr_query(query, employee, leave_mgr)
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue

if __name__ == "__main__":
    main()