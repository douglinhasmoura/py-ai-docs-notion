import requests
from typing import List, Dict, Any

class NotionAPIClient:
    def __init__(self, token: str, version: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": version,
            "Content-Type": "application/json"
        }
    
    def get_block_children(self, block_id: str) -> List[Dict[str, Any]]:
        """Busca blocos filhos com paginação"""
        url = f"https://api.notion.com/v1/blocks/{block_id}/children"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json().get("results", [])
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar bloco {block_id}: {e}")
            return []