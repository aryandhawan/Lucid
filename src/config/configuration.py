from utils.common import *
from entity.ingestion_config import IngestionConfig
from entity.relevance_config import RelevanceConfig
from entity.summarization_config import SummarizationConfig
from entity.vectorstore_config import VectorStoreConfig
from entity.email_config import EmailConfig
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
    
    def get_summarization_config(self):
        summarization_config = SummarizationConfig(
            model_name=self.config.summarization.model_name,
            temperature=self.config.summarization.temperature,
            max_summary_tokens=self.config.summarization.max_summary_tokens,
            tier=self.config.summarization.tier
            )
        
        return summarization_config

    def get_vectorstore_config(self):
        vectorstore_config = VectorStoreConfig(
            embedding_model=self.config.vectorstore.embedding_model,
            vectorstore_type=self.config.vectorstore.vectorstore_type,
            device=self.config.vectorstore.device,
            collection_name_papers=self.config.vectorstore.collection_name_papers,
            persist_directory=self.config.vectorstore.persist_directory,
            top_k=self.config.vectorstore.top_k,
            chunk_size=self.config.vectorstore.chunk_size,
            chunk_overlap=self.config.vectorstore.chunk_overlap
        )
        return vectorstore_config
    
    def get_email_config(self):
        email_config = EmailConfig(
            sender_email=self.config.email.sender_email,
            recipient_email=self.config.email.recipient_email,
            subject_template=self.config.email.subject_template
        )
        return email_config
