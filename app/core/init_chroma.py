# app/core/init_chroma.py

import os
import pandas as pd
import shutil
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document

class LangChainSentenceTransformer:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        return self.model.encode(texts, show_progress_bar=True).tolist()

    def embed_query(self, text):
        return self.model.encode([text])[0]

def init_db(csv_filename="dataset_question.csv", persist_directory="./db"):
    if not os.path.exists(csv_filename):
        raise FileNotFoundError(f"{csv_filename} 파일이 없습니다.")
    
    df = pd.read_csv(csv_filename)

    documents = [
        Document(
            page_content=f"{row['질문']} [기업명: {row['기업명']}, 경력: {row['경력']}, 직무: {row['직무']}]",
            metadata={"기업명": row["기업명"], "경력": row["경력"], "직무": row["직무"]}
        )
        for _, row in df.iterrows()
        if pd.notna(row["질문"]) and row["질문"].strip() != ""
    ]

    embedder = LangChainSentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
    
    db = Chroma.from_documents(documents, embedder, persist_directory=persist_directory)
    print(f"✅ DB 초기화 완료. 총 문서 수: {len(documents)}")

# CLI 실행용
if __name__ == "__main__":
    init_db()
