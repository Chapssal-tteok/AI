from app.core.vector_utils import get_chroma_db

def search_similar_questions(query: str):
    db = get_chroma_db()
    results = db.similarity_search(query, k=3)
    return [
        {
            "content": doc.page_content,
            "metadata": doc.metadata
        }
        for doc in results
    ]