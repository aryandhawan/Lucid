from dataclasses import dataclass

@dataclass(frozen=True)
class IngestionConfig:
    arxiv_categories: list[str]
    max_results_per_category: int
    days_back: int
