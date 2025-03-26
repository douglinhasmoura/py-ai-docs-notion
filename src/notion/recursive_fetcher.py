import time
from typing import List, Dict, Any

class RecursiveFetcher:
    def __init__(self, api_client, parser, delay: float = 0.3):
        self.api_client = api_client
        self.parser = parser
        self.delay = delay
    
    def fetch_page(self, page_id: str, max_depth: int = 2) -> str:
        """Busca conteúdo recursivamente"""
        blocks = self.api_client.get_block_children(page_id)
        content = []
        
        for block in blocks:
            parsed = self.parser.parse_block(block)
            if parsed:
                content.append(parsed)
            
            if block.get("has_children"):
                time.sleep(self.delay)
                child_content = self.fetch_page(block["id"], max_depth-1)
                if child_content:
                    content.append(child_content)
        
        return "\n".join(content)