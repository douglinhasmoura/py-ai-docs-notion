from dotenv import load_dotenv
import os
from src.notion import NotionAPIClient, RecursiveFetcher, NotionBlockParser
from src.chroma import ChromaRetriever

load_dotenv()

# Configuração
notion = NotionAPIClient(os.getenv("NOTION_TOKEN"), os.getenv("NOTION_VERSION"))
parser = NotionBlockParser()
fetcher = RecursiveFetcher(notion, parser)

# Busca conteúdo
page_id = os.getenv("NOTION_PAGE_ID")
content = fetcher.fetch_page(page_id)

# Indexação
retriever = ChromaRetriever()
db = retriever.create_from_texts([content])
print("Conteúdo indexado com sucesso!")