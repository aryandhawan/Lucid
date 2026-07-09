from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class SummarizationConfig:
    """Class to hold the summarization configuration for research papers."""
    model_name: str
    temperature: float
    max_summary_tokens: int
    tier: str