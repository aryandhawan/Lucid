from utils.common import *
from entity.ingestion_config import IngestionConfig
from entity.relevance_config import RelevanceConfig
class ConfigurationManager:
    def __init__(self, config_filepath: Path = Path("config/config.yaml")):
        self.config = read_yaml(config_filepath)

    # methods from here!

    def get_ingestion_config(self)->IngestionConfig:
        ingestion_config = IngestionConfig(
            arxiv_categories=self.config.ingestion.arxiv_categories,
            max_results_per_category=self.config.ingestion.max_results_per_category,
            days_back=self.config.ingestion.days_back
        )
        return ingestion_config
    
    def get_relevance_config(self)->RelevanceConfig:
        relevance_config = RelevanceConfig(
            interest_profile=self.config.relevance.interest_profile,
            relevance_threshold=self.config.relevance.relevance_threshold,
            model_name=self.config.relevance.model_name,
            temperature=self.config.relevance.temperature
        )
        return relevance_config