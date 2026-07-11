from dataclasses import dataclass
from pathlib import Path

@dataclass
class EmailConfig:
    sender_email: str
    recipient_email: list[str]
    subject_template: str