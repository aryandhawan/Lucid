from src.components.vectorstore import VectorStore
from langchain_core.documents import Document
from typing import Optional


class RetrievalService:
    def __init__(self, vectorstore: VectorStore):
        self.vectorstore = vectorstore

    def retrieve_documents(
        self,
        search_query: str,
        retrieval_mode: str,          
        anchor_paper_id: Optional[str] = None,
        top_k: int = 5
    ) -> list[Document]:

        if retrieval_mode == "single_paper" and anchor_paper_id:
            retriever = self.vectorstore.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": top_k, "filter": {"arxiv_id": anchor_paper_id}}
            )
        else:
            retriever = self.vectorstore.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": top_k}
            )

        return retriever.invoke(search_query)