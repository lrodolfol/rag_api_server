from dataclasses import dataclass
from typing import Optional


@dataclass
class RagEmail:
    from_: str
    to: str
    subject: str
    sender: str
    copy_to: str
    message: str
    html_message: Optional[str] = None
