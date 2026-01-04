from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: Optional[int] = None
    name: str = ""
    company: str = ""
    email: str = ""
    phone: Optional[str] = None
    code: str = ""
    code_used: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_premium: Optional[bool] = None
    free_test: Optional[bool] = None
    expired: Optional[bool] = None