from dataclasses import dataclass

@dataclass
class VectorStoreConfig:
    embedding_model: str
    vectorstore_type: str
    device: str
    collection_name_papers: str
    persist_directory: str
    top_k: int
    chunk_size: int
    chunk_overlap: int