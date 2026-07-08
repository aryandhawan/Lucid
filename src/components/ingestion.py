import arxiv
from datetime import datetime, timedelta
from entity.ingestion_config import IngestionConfig


class ArxivFetcher:
    def __init__(self, ingestion_config: IngestionConfig):
        self.ingestion_config = ingestion_config
        self.client = arxiv.Client(delay_seconds=3,num_retries=3)  # Adjust delay and retries as needed

    def find_research_papers(self) -> list[dict]:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=self.ingestion_config.days_back)

        seen_ids = set()
        collected_papers = []

        for category in self.ingestion_config.arxiv_categories:
            search = arxiv.Search(
                query=f"cat:{category} AND submittedDate:[{start_date.strftime('%Y%m%d%H%M')} TO {end_date.strftime('%Y%m%d%H%M')}]",
                max_results=self.ingestion_config.max_results_per_category,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )

            results = self.client.results(search)

            for paper in results:
                clean_id = paper.entry_id.split("/abs/")[-1]  # strips URL, keeps e.g. "2401.12345v1"

                if clean_id in seen_ids:
                    continue  # already fetched via another category
                seen_ids.add(clean_id)

                collected_papers.append({
                    "arxiv_id": clean_id,
                    "title": paper.title,
                    "abstract": paper.summary,
                    "authors": [author.name for author in paper.authors],
                    "published": paper.published,
                    "pdf_url": paper.pdf_url,
                    "categories": paper.categories,
                })

        return collected_papers
    
if __name__ == "__main__":
    ingestion_config = IngestionConfig(
        arxiv_categories=["cs.AI", "cs.LG"],
        max_results_per_category=5,
        days_back=7
    )
    fetcher = ArxivFetcher(ingestion_config)
    papers = fetcher.find_research_papers()
    print(f"Total papers fetched: {len(papers)}")
    print(papers[6])  # inspect one full record