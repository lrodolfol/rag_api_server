from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: int
    name: str
    company: str
    email: str
    phone: str
    code: str
    code_used: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    is_premium: bool
    free_test: bool
