import re

def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"<[^>]+>", "", text)   # remove HTML
    text = re.sub(r"\s+", " ", text)      # normalize spaces
    return text.strip()

def prepare_news_text(title, content):
    return clean_text(f"{title}. {content}")
