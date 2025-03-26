import requests
import time
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import os
from langchain_core.documents import Document
from langchain.vectorstores import Chroma 
from langchain.embeddings import HuggingFaceEmbeddings

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_VERSION = os.getenv("NOTION_VERSION")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json"
}

def get_block_children(block_id: str, delay: float = 0.3) -> List[Dict[str, Any]]:
    """Obtém todos os blocos filhos de um bloco, recursivamente com tratamento melhorado"""
    url = f"https://api.notion.com/v1/blocks/{block_id}/children?page_size=100"
    
    all_blocks = []
    next_cursor = None
    
    while True:
        try:
            params = {}
            if next_cursor:
                params["start_cursor"] = next_cursor
                
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            for block in data.get("results", []):
                all_blocks.append(block)
                
                # Processa filhos recursivamente se existirem
                if block.get("has_children", False) and block["type"] not in ["child_page", "child_database"]:
                    time.sleep(delay)
                    child_blocks = get_block_children(block["id"], delay)
                    all_blocks.extend(child_blocks)
            
            if not data.get("has_more", False):
                break
                
            next_cursor = data.get("next_cursor")
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar bloco {block_id}: {e}")
            break
    
    return all_blocks

def extract_text_from_rich_text(rich_text: List[Dict[str, Any]]) -> str:
    """Extrai texto formatado de rich_text com marcações especiais"""
    text_parts = []
    for text in rich_text:
        content = text.get("plain_text", "")
        annotations = text.get("annotations", {})
        
        # Adiciona marcações baseadas em anotações
        if annotations.get("bold"):
            content = f"**{content}**"
        if annotations.get("italic"):
            content = f"*{content}*"
        if annotations.get("code"):
            content = f"`{content}`"
        
        text_parts.append(content)
    
    return "".join(text_parts)

def extract_content_from_blocks(blocks: List[Dict[str, Any]]) -> str:
    """Extrai texto formatado dos blocos do Notion com metadados estruturados"""
    content = []
    
    for block in blocks:
        block_type = block["type"]
        content_data = block.get(block_type, {})
        
        # Cabeçalhos
        if block_type.startswith("heading_"):
            level = int(block_type.split("_")[1])
            prefix = "#" * level
            text = extract_text_from_rich_text(content_data.get("rich_text", []))
            content.append(f"{prefix} {text}")
        
        # Listas
        elif block_type in ["bulleted_list_item", "numbered_list_item"]:
            prefix = "-" if block_type == "bulleted_list_item" else "1."
            text = extract_text_from_rich_text(content_data.get("rich_text", []))
            content.append(f"{prefix} {text}")
        
        # Citações e callouts
        elif block_type in ["quote", "callout"]:
            text = extract_text_from_rich_text(content_data.get("rich_text", []))
            icon = content_data.get("icon", {}).get("emoji", "") if block_type == "callout" else ">"
            content.append(f"{icon} {text}")
        
        # Código
        elif block_type == "code":
            text = extract_text_from_rich_text(content_data.get("rich_text", []))
            language = content_data.get("language", "")
            content.append(f"```{language}\n{text}\n```")
        
        # Texto simples
        elif "rich_text" in content_data:
            text = extract_text_from_rich_text(content_data["rich_text"])
            if text.strip():
                content.append(text)
        
        # Adiciona separador entre blocos
        if content and content[-1].strip():
            content.append("\n")
    
    return "\n".join(content).strip()

def get_page_content_recursive(page_id: str, max_depth: int = 3, current_depth: int = 0) -> str:
    """Obtém todo o conteúdo de uma página do Notion recursivamente"""
    if current_depth >= max_depth:
        return ""
    
    blocks = get_block_children(page_id)
    content = extract_content_from_blocks(blocks)
    
    # Processa páginas filhas
    child_pages = [b for b in blocks if b["type"] == "child_page"]
    for page in child_pages:
        time.sleep(0.3)
        child_content = get_page_content_recursive(page["id"], max_depth, current_depth + 1)
        if child_content:
            content += f"\n\n## {page.get('child_page', {}).get('title', 'Subpágina')}\n\n{child_content}"
    
    return content

def get_page_content(page_id: str) -> str:
    """Wrapper para compatibilidade com versão anterior"""
    return get_page_content_recursive(page_id)

def setup_retriever(texts: List[str], metadata: Optional[List[Dict[str, Any]]] = None, 
                   embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
    """
    Configura o ChromaDB retriever com tratamento melhorado
    
    Args:
        texts: Lista de textos para indexar
        metadata: Lista de metadados correspondentes
        embedding_model: Modelo de embeddings
    """
    # Cria documentos LangChain
    if metadata is None:
        metadata = [{} for _ in texts]
    
    documents = [
        Document(page_content=text, metadata=meta)
        for text, meta in zip(texts, metadata)
    ]
    
    # Configura embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=embedding_model,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    # Configura ChromaDB
    db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="database/chroma",
        collection_metadata={
            "hnsw:space": "cosine",
            "allow_updates": True
        }
    )
    
    # Configura retriever com MMR (Maximum Marginal Relevance)
    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={
            'k': 6,
            'fetch_k': 20,
            'lambda_mult': 0.5,
            'filter': {'source': {'$exists': True}}
        }
    )
    
    return retriever