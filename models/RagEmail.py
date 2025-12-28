from dataclasses import dataclass

@dataclass
class RagEmail:
    from_: str
    to: str
    subject: str
    sender: str
    copy_to: str
    message: str
