# src/hr_specific/leave_manager.py
from datetime import datetime
from src.data_models.leave import LeaveRequest, LeaveStatus, LeaveType

class LeaveManager:
    def __init__(self, employee_db):
        self.employee_db = employee_db
        self.leave_requests = []
    
    def check_leave_balance(self, employee_id):
        """Get employee's leave balance"""
        employee = self.employee_db.get_employee(employee_id)
        if employee:
            return employee.leave_balance
        return 0
    
    def apply_for_leave(self, employee_id, leave_type, from_date, to_date, reason):
        """Submit a leave request"""
        employee = self.employee_db.get_employee(employee_id)
        
        if not employee:
            return {"status": "error", "message": "Employee not found"}
        
        # Check if leave balance sufficient
        days_requested = (to_date - from_date).days
        if days_requested > employee.leave_balance:
            return {
                "status": "error",
                "message": f"Insufficient leave balance. Available: {employee.leave_balance}, Requested: {days_requested}"
            }
        
        # Create leave request
        request_id = f"LR_{len(self.leave_requests) + 1:04d}"
        leave_req = LeaveRequest(
            request_id=request_id,
            employee_id=employee_id,
            leave_type=leave_type,
            from_date=from_date,
            to_date=to_date,
            reason=reason
        )
        
        self.leave_requests.append(leave_req)
        
        return {
            "status": "success",
            "message": f"Leave request submitted: {request_id}",
            "request_id": request_id
        }
    
    def approve_leave(self, request_id, approved_by):
        """Approve a leave request"""
        for req in self.leave_requests:
            if req.request_id == request_id:
                req.status = LeaveStatus.APPROVED.value
                req.approved_by = approved_by
                
                # Deduct from employee's balance
                employee = self.employee_db.get_employee(req.employee_id)
                days = (req.to_date - req.from_date).days
                employee.leave_balance -= days
                
                return {"status": "success", "message": "Leave approved"}
        
        return {"status": "error", "message": "Request not found"}
    
    def reject_leave(self, request_id, approved_by):
        """Reject a leave request"""
        for req in self.leave_requests:
            if req.request_id == request_id:
                req.status = LeaveStatus.REJECTED.value
                req.approved_by = approved_by
                return {"status": "success", "message": "Leave rejected"}
        
        return {"status": "error", "message": "Request not found"}
    
    def get_pending_requests(self):
        """Get all pending leave requests"""
        return [r for r in self.leave_requests if r.status == LeaveStatus.PENDING.value]