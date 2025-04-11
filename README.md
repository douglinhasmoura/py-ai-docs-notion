# 📝 Notion Chat with Google Gemini

✨ A powerful AI chatbot that answers questions based on your Notion pages, powered by Google Gemini and ChromaDB!

This Python application lets you query your Notion pages in natural language and get accurate answers using Google Gemini for AI responses and ChromaDB for efficient document storage and retrieval.


---

## 🔧 Features

✅ Chat Interface - Talk to your Notion pages using Gradio for a user-friendly UI.

✅ Google Gemini AI - Leverages LangChain & Gemini Pro for high-quality responses.

✅ ChromaDB Vector Storage - Efficiently stores and retrieves embeddings from Notion.

✅ Environment Variables - Securely manage API keys with .env.

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/douglinhasmoura/notion-gemini-chat.git
cd py-ai-docs-notion
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
```python
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\activate   # Windows
```

### 3. Install Dependencies
```python
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a .env file like .env.example

(Get your keys from [Notion Developers](https://developers.notion.com/) and [Google AI Studio](https://aistudio.google.com/).)

## 🚀 Usage

### 1. Run the chat interface

``` python
python app.py
```

Gradio will launch a local interface


## 🛠️ Tech Stack
* AI & NLP: Google Gemini (langchain_google_genai)

* Vector Database: ChromaDB (via langchain_community)

* Chat Interface: Gradio

* Notion API: requests

* Environment Management: python-dotenv


## 📁 Project Structure

```python
 py-ai-docs-notion/
    ├── src/
       ├── chroma/
            ├── __init__.py
            └── retriever.py
       ├── frontend/
            ├── __init__.py
            ├── components.py
            └── utils.py
       ├── notion/  
            ├── __init__.py
            ├── agent.py
            ├── api_client.py
            ├── block_parser.py
            └── recursive_fetcher.py 
       └── utils/
            ├── __init__.py
            ├── llm.py
            ├── logging.py
            ├── notion.py
            └── text_processor.py
        __init__.py
    ├── app.py
    ├── main.py
    ├── .env.example
    ├── requirements.txt
    └── README.md

```

🤝 Collaborators:

[Douglas Moura](https://github.com/douglinhasmoura)
