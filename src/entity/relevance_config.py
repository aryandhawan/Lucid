from dataclasses import dataclass, field
from typing import List, Optional

@dataclass(frozen=True)
class RelevanceConfig:
    """Class to hold the relevance configuration for research papers."""

    interest_profile: List[str]
    relevance_threshold: int
    model_name: str
    temperature: float