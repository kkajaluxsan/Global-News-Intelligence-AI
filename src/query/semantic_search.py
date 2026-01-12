import os
from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_search(query, top_k=5):
    # Encode query and keep as Python list
    query_embedding = model.encode(query).tolist()

    with engine.begin() as conn:
        results = conn.execute(
            text("""
                SELECT 
                    r.title,
                    r.source,
                    r.url,
                    1 - (e.embedding <=> CAST(:query_embedding AS vector)) AS similarity
                FROM news_embeddings e
                JOIN raw_news r ON r.id = e.news_id
                ORDER BY e.embedding <=> CAST(:query_embedding AS vector)
                LIMIT :top_k
            """),
            {
                "query_embedding": query_embedding,
                "top_k": top_k
            }
        ).fetchall()

    return results

if __name__ == "__main__":
    q = input("🔎 Ask about global news: ")
    results = semantic_search(q)

    for r in results:
        print(f"\n📰 {r.title}")
        print(f"Source: {r.source}")
        print(f"Similarity: {round(r.similarity, 3)}")
        print(f"URL: {r.url}")
