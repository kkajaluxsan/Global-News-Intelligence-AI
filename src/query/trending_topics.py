import os
import re
from collections import Counter
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

STOPWORDS = set([
    "the", "and", "to", "of", "in", "on", "for", "with", "as",
    "is", "are", "was", "were", "by", "from", "at", "an", "a",
    "after", "over", "into", "that", "this", "it"
])

def clean_words(text):
    words = re.findall(r"[a-zA-Z]{4,}", text.lower())
    return [w for w in words if w not in STOPWORDS]

def get_trending_topics(limit=6):
    with engine.begin() as conn:
        rows = conn.execute(
            text("""
                SELECT title, content
                FROM raw_news
                ORDER BY published_at DESC
                LIMIT 100
            """)
        ).fetchall()

    counter = Counter()

    for r in rows:
        combined = f"{r.title or ''} {r.content or ''}"
        counter.update(clean_words(combined))

    return [word for word, _ in counter.most_common(limit)]
