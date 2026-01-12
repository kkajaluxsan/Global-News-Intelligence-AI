import os
from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from src.transform.prepare_text import prepare_news_text

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(limit=100):
    with engine.begin() as conn:
        rows = conn.execute(
            text("""
                SELECT id, title, content
                FROM raw_news
                WHERE id NOT IN (
                    SELECT news_id FROM news_embeddings
                )
                LIMIT :limit
            """),
            {"limit": limit}
        ).fetchall()

        if not rows:
            print("✅ No new articles to embed")
            return

        texts = [
            prepare_news_text(r.title, r.content)
            for r in rows
        ]

        embeddings = model.encode(texts)

        for row, emb in zip(rows, embeddings):
            conn.execute(
                text("""
                    INSERT INTO news_embeddings (news_id, embedding)
                    VALUES (:news_id, :embedding)
                """),
                {
                    "news_id": row.id,
                    "embedding": emb.tolist()
                }
            )

        print(f"🤖 Embedded {len(rows)} articles")

if __name__ == "__main__":
    generate_embeddings()
