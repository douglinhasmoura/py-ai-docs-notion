"""
Módulo principal do Notion Helper

Exporta os componentes principais para uso externo:
"""
from .notion import NotionAPIClient, RecursiveFetcher  # Exemplo
from .chroma import ChromaRetriever

__version__ = "0.1.0"
__all__ = ['NotionAPIClient', 'RecursiveFetcher', 'ChromaRetriever']  # Controla o que é importado com `from src import *`