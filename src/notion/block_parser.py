from typing import List, Dict, Any

class NotionBlockParser:
    @staticmethod
    def _extract_rich_text(rich_text: List[Dict[str, Any]]) -> str:
        """Extrai texto formatado com markdown básico"""
        text_parts = []
        for text in rich_text:
            content = text.get("plain_text", "")
            if text.get("annotations", {}).get("bold"):
                content = f"**{content}**"
            text_parts.append(content)
        return "".join(text_parts)

    def parse_block(self, block: Dict[str, Any]) -> str:
        """Processa um bloco individual"""
        block_type = block["type"]
        content = block.get(block_type, {})
        
        if "rich_text" in content:
            return self._extract_rich_text(content["rich_text"])
        return ""