# src/notion/agent.py
import os
from typing import List
from src.utils.llm import load_llm
from .api_client import NotionAPIClient
from .block_parser import NotionBlockParser
from .recursive_fetcher import RecursiveFetcher
from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

class NotionAgent:
    def __init__(self):
        self.llm = load_llm() 
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.api_client = NotionAPIClient(os.getenv("NOTION_TOKEN"), os.getenv("NOTION_VERSION"))
        self.parser = NotionBlockParser()
        self.fetcher = RecursiveFetcher(self.api_client, self.parser)
        
        # Carrega conteúdo
        content = self.fetcher.fetch_page(os.getenv("DEFAULT_PAGE_ID"))
        
        # Configura ChromaDB
        self.vectorstore = Chroma.from_texts(
            texts=[content],
            embedding=self.embeddings,
            persist_directory="database/chroma"
        )
    
    def respond(self, question: str, history: List) -> str:
        try:
            if not question.strip():
                return "Por favor, faça uma pergunta válida."
            
            # Garante que a cadeia QA está inicializada
            if not hasattr(self, 'qa_chain'):
                self._initialize_qa_chain()
                
            result = self.qa_chain({"question": question, "chat_history": history})
            return result.get("answer", "Não foi possível gerar uma resposta.")
            
        except Exception as e:
            print(f"Erro ao processar pergunta: {e}")
            return f"Erro ao processar sua pergunta: {str(e)}"

    def _initialize_qa_chain(self):
        """Inicializa a cadeia de QA se não existir"""
        from langchain.chains import ConversationalRetrievalChain
        from langchain.memory import ConversationBufferMemory
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(),
            memory=self.memory,
            verbose=True
        )