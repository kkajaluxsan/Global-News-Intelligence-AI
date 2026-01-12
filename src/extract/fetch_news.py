import feedparser
from datetime import datetime
import json
import os

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL connection
engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

NEWS_FEEDS = {
    "bbc": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "reuters": "http://feeds.reuters.com/reuters/worldNews",
    "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml"
}


def fetch_news():
    articles = []

    for source, url in NEWS_FEEDS.items():
        feed = feedparser.parse(url)

        for entry in feed.entries:
            articles.append({
                "source": source,
                "title": entry.get("title"),
                "content": entry.get("summary", ""),
                "url": entry.get("link"),
                "published_at": entry.get("published", None),
                "raw_json": json.dumps(entry)
            })

    return articles


def load_news_to_db(articles):
    inserted = 0

    with engine.begin() as conn:
        for article in articles:
            if not article["url"] or not article["title"]:
                continue  # safety skip

            result = conn.execute(
                text("""
                    INSERT INTO raw_news (
                        source, title, content, url, published_at, raw_json
                    )
                    VALUES (
                        :source, :title, :content, :url, :published_at, :raw_json
                    )
                    ON CONFLICT (url) DO NOTHING
                """),
                article
            )

            # rowcount = 1 only if actually inserted
            if result.rowcount == 1:
                inserted += 1

    return inserted


if __name__ == "__main__":
    news = fetch_news()
    print(f"📰 Fetched {len(news)} articles")

    inserted_count = load_news_to_db(news)
    print(f"✅ Inserted {inserted_count} new articles into raw_news")
