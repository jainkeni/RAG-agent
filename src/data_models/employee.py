# src/data_models/employee.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Employee:
    employee_id: str
    name: str
    email: str
    department: str
    designation: str
    joining_date: datetime
    leave_balance: int = 20
    manager: str = None
    
    def __repr__(self):
        return f"Employee({self.name}, {self.employee_id}, {self.department})"