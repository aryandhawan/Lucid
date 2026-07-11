from src.entity.vectorstore_config import VectorStoreConfig
from src.utils.common import *
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class VectorStore:
    def __init__(self, config: VectorStoreConfig):
        self.config = config

        self.embedding_model = HuggingFaceEmbeddings(
            model_name=self.config.embedding_model,
            model_kwargs={"device": self.config.device},
            encode_kwargs={"normalize_embeddings": True}
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
        )

        self.vectorstore = Chroma(
            collection_name=self.config.collection_name_papers,
            persist_directory=self.config.persist_directory,
            embedding_function=self.embedding_model
        )

    def create_vectorstore(self, summary, relevance_score, documents: dict):
        doc = Document(
            page_content=documents["abstract"],
            metadata={
                "arxiv_id": documents["arxiv_id"],
                "title": documents["title"],
                "summary": summary,
                "relevance_score": relevance_score,
                "published": str(documents["published"]),
                "pdf_url": documents["pdf_url"],
            }
        )

        self.vectorstore.add_documents([doc])