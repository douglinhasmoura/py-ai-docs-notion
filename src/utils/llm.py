from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

def load_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.3,
        api_key=os.getenv("GOOGLE_API_KEY")
    )

def load_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        api_key=os.getenv("GOOGLE_API_KEY")
    )