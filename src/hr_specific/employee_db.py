# src/hr_specific/employee_db.py
import csv
from datetime import datetime
from src.data_models.employee import Employee

class EmployeeDatabase:
    def __init__(self, csv_path="data/employee_data/employees.csv"):
        self.csv_path = csv_path
        self.employees = self.load_employees()
    
    def load_employees(self):
        """Load employees from CSV"""
        employees = {}
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    emp = Employee(
                        employee_id=row['employee_id'],
                        name=row['name'],
                        email=row['email'],
                        department=row['department'],
                        designation=row['designation'],
                        joining_date=datetime.strptime(row['joining_date'], '%Y-%m-%d'),
                        leave_balance=int(row.get('leave_balance', 20)),
                        manager=row.get('manager')
                    )
                    employees[emp.employee_id] = emp
        except FileNotFoundError:
            print(f"⚠️  Employee file not found: {self.csv_path}")
        except Exception as e:
            print(f"❌ Error loading employees: {e}")
        return employees
    
    def get_employee(self, employee_id):
        """Get employee by ID"""
        return self.employees.get(employee_id)
    
    def get_all_employees(self):
        """Get all employees"""
        return list(self.employees.values())
    
    def add_employee(self, employee):
        """Add new employee"""
        self.employees[employee.employee_id] = employee
    
    def get_employee_by_email(self, email):
        """Get employee by email"""
        for emp in self.employees.values():
            if emp.email == email:
                return emp
        return None