# src/data_models/leave.py
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class LeaveStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class LeaveType(Enum):
    ANNUAL = "annual"
    SICK = "sick"
    CASUAL = "casual"
    MATERNITY = "maternity"

@dataclass
class LeaveRequest:
    request_id: str
    employee_id: str
    leave_type: str
    from_date: datetime
    to_date: datetime
    reason: str
    status: str = LeaveStatus.PENDING.value
    applied_on: datetime = field(default_factory=datetime.now)
    approved_by: str = None