import os
from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

# DB
engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Models
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def search_articles(query, top_k=12):
    query_embedding = embed_model.encode(query).tolist()

    with engine.begin() as conn:
        rows = conn.execute(
            text("""
                SELECT r.source, r.content
                FROM news_embeddings e
                JOIN raw_news r ON r.id = e.news_id
                ORDER BY e.embedding <=> (:query_embedding)::vector
                LIMIT :top_k
            """),
            {"query_embedding": query_embedding, "top_k": top_k}
        ).fetchall()

    return rows

def summarize_by_source(query):
    rows = search_articles(query)

    grouped = defaultdict(list)
    for r in rows:
        if r.content:
            grouped[r.source].append(r.content)

    summaries = {}
    for source, texts in grouped.items():
        combined_text = " ".join(texts)[:3500]  # model-safe length

        summary = summarizer(
            combined_text,
            max_length=130,
            min_length=60,
            do_sample=False
        )[0]["summary_text"]

        summaries[source] = summary

    return summaries

if __name__ == "__main__":
    q = input("🔎 Topic: ")
    results = summarize_by_source(q)

    for source, summary in results.items():
        print(f"\n📰 {source.upper()} SUMMARY:")
        print(summary)
