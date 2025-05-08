from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma
from app.core.config import settings

class LangChainSentenceTransformer:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        return self.model.encode(texts, show_progress_bar=False).tolist()

    def embed_query(self, text):
        return self.model.encode([text])[0]

def get_chroma_db():
    embedding_function = LangChainSentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    return Chroma(persist_directory="./db", embedding_function=embedding_function)