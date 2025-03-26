from src.utils.llm import load_embeddings, load_llm
from .agent import NotionAgent
from .api_client import NotionAPIClient
from .block_parser import NotionBlockParser
from .recursive_fetcher import RecursiveFetcher

__all__ = ['NotionAgent', 'NotionAPIClient', 'NotionBlockParser', 'RecursiveFetcher']

def __init__(self):
    self.llm = load_llm()
    self.embeddings = load_embeddings()
    self._initialize_vectorstore()
    self._initialize_qa_chain()  # Garante que a cadeia existe
