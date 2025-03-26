from typing import List
from langchain_core.documents import Document
from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

class ChromaRetriever:
    def __init__(self, embedding_model: str = None):
        self.embedding_model = embedding_model or "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    
    def create_from_texts(self, texts: List[str]) -> Chroma:
        """Cria vetorstore a partir de textos"""
        embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model,
            model_kwargs={'device': 'cpu'}
        )
        
        return Chroma.from_texts(
            texts=texts,
            embedding=embeddings,
            persist_directory="database/chroma"
        )