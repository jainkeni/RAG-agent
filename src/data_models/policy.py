# src/data_models/policy.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Policy:
    policy_id: str
    title: str
    description: str
    effective_date: datetime
    version: str
    content: str