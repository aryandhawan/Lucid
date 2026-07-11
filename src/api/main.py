import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from src.config.configuration import ConfigurationManager
from src.pipeline.ingestion_pipeline import IngestionPipeline
from src.components.email_sender import EmailDigestSender  # once built

def main():
    config_manager = ConfigurationManager()
    pipeline = IngestionPipeline(config_manager)
    digest_papers = pipeline.run()
    

    email_config = config_manager.get_email_config()
    sender = EmailDigestSender(email_config)
    sender.send_digest(digest_papers)

if __name__ == "__main__":
    main()
