from src.components.ingestion import ArxivFetcher
from src.components.relevance_gate import RelevanceClassifier
from src.components.summarizer import Summarizer
from src.components.vectorstore import VectorStore



class IngestionPipeline:
    def __init__(self, config_manager):
        ingestion_config = config_manager.get_ingestion_config()
        relevance_config = config_manager.get_relevance_config()
        summarization_config = config_manager.get_summarization_config()
        vectorstore_config = config_manager.get_vectorstore_config()

        self.fetcher = ArxivFetcher(ingestion_config)
        self.classifier = RelevanceClassifier(relevance_config)
        self.summarizer = Summarizer(summarization_config)
        self.vectorstore = VectorStore(vectorstore_config)

    def run(self) -> list[dict]:
        papers = self.fetcher.find_research_papers()
        print(f"DEBUG papers fetched: {len(papers)}")

        digest_papers = []
        for paper in papers:
            if self.vectorstore.exists(paper["arxiv_id"]):
                print(f"DEBUG skipping already-seen: {paper['title'][:50]}")
                continue  # already processed in a previous run, skip entirely

            score = self.classifier.classify_relevance(paper)
            if not self.classifier.is_relevant(score):
                continue

            summary = self.summarizer.summarize(paper)
            self.vectorstore.create_vectorstore(summary, score, paper)

            digest_papers.append({
                "title": paper["title"],
                "summary": summary,
                "arxiv_id": paper["arxiv_id"],
                "pdf_url": paper["pdf_url"],
                "relevance_score": score,
            })

        return digest_papers
        