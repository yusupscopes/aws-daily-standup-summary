from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    title: str
    description: str
    status: str
    source: str # JIRA, GITLAB, etc.
    url: Optional[str] = None
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None