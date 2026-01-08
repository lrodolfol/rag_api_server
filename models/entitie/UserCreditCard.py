from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserCreditCard:
    id: Optional[int] = None
    completed_name: str = ""
    number: int = None
    validity: str = ""
    client_id: int = None