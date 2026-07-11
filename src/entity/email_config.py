from dataclasses import dataclass
from pathlib import Path

@dataclass
class EmailConfig:
    sender_email: str
    recipient_email: str
    subject_template: str