# src/hr_specific/hr_utils.py
"""HR-specific utility functions"""
from datetime import datetime

def get_personalized_prompt(employee_name, query):
    """Generate HR-specific prompt with employee context"""
    prompt = f"""
You are an HR Assistant for the company.
You're helping {employee_name} with their HR-related query.

Use the context below to answer the question. Focus on company policies and procedures.
Provide clear, structured answers with relevant policy references when applicable.

Question from employee: {query}

Provide a helpful and professional response.
"""
    return prompt

def format_leave_info(employee, leave_manager):
    """Format employee leave information"""
    balance = leave_manager.check_leave_balance(employee.employee_id)
    return f"""
Employee Leave Info:
- Name: {employee.name}
- Available Leave: {balance} days
- Department: {employee.department}
- Reporting Manager: {employee.manager}
"""

def validate_date_range(from_date, to_date):
    """Validate leave date range"""
    if from_date >= to_date:
        return False, "From date must be before to date"
    
    if from_date < datetime.now():
        return False, "Cannot apply leave for past dates"
    
    return True, "Valid date range"