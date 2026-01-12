# 🌍 Global News Intelligence AI

**Global News Intelligence AI** is an end-to-end AI-powered platform that ingests global news, transforms articles into neural embeddings, and enables semantic understanding and similarity-based search using vector databases. Instead of relying on keyword matching, this system understands *meaning* and *context* in news content.

> **From raw news to semantic intelligence**

---

## 🚀 Features

- 📰 **Automated News Ingestion**  
  Fetches global news articles from RSS feeds and other sources.

- 🧹 **Text Cleaning & Normalization**  
  Cleans raw HTML content and prepares text for downstream NLP tasks.

- 🤖 **Neural Text Embeddings**  
  Converts news articles into dense vector representations using Sentence Transformers.

- 🧠 **Vector Database (pgvector)**  
  Stores embeddings efficiently inside PostgreSQL for scalable similarity search.

- 📐 **Cosine / Vector Similarity Search**  
  Retrieves semantically similar news articles based on meaning, not keywords.

- 🌐 **Semantic Understanding**  
  Enables contextual search, clustering, and future trend analysis.

---

## 🏗️ System Architecture

```
RSS / News Sources
        ↓
   Data Ingestion
        ↓
   Text Cleaning
        ↓
 Neural Embeddings
        ↓
  Vector Database
        ↓
 Semantic Search
```

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **PostgreSQL**
- **pgvector** (vector similarity search)
- **Sentence-Transformers**
- **Hugging Face Transformers**
- **psycopg2 / SQLAlchemy**
- **Regex / NLP preprocessing**

---

## 📂 Project Structure

```
Global-News-Intelligence-AI/
│
├── src/
│   ├── extract/
│   │   └── fetch_news.py        # News ingestion
│   ├── transform/
│   │   ├── prepare_text.py      # Text cleaning & preparation
│   │   └── embed_news.py        # Embedding generation
│   └── search/
│       └── semantic_search.py   # Vector similarity search
│
├── sql/
│   └── schema.sql               # Database schema
│
├── .env                         # Environment variables
├── requirements.txt
└── README.md
```

---

## 🗄️ Database Schema

### `raw_news`
Stores original news articles and metadata.

- `id` (PK)
- `source`
- `title`
- `content`
- `url` (unique)
- `published_at`
- `language`
- `country`
- `raw_json`

### `processed_news`
Stores cleaned and enriched text.

- `news_id` (FK)
- `cleaned_text`
- `sentiment`
- `topic`
- `summary`

### `news_embeddings`
Stores vector embeddings.

- `news_id` (FK)
- `embedding` (VECTOR)

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/Global-News-Intelligence-AI.git
cd Global-News-Intelligence-AI
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file:

```
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=global_news_ai
```

### 5️⃣ Setup Database

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Run schema:

```bash
psql -U postgres -d global_news_ai -f sql/schema.sql
```

---

## ▶️ Usage

### Fetch News

```bash
python -m src.extract.fetch_news
```

### Generate Embeddings

```bash
python -m src.transform.embed_news
```

### Semantic Search

```bash
python -m src.search.semantic_search
```

Example output:

```
📰 Trump mulls 'very strong' military options
Source: BBC
Similarity: 0.87
URL: https://www.bbc.com/news/articles/...
```

---

## 📈 Future Enhancements

- 🔍 Advanced filtering (date, country, source)
- 📊 Topic clustering & trend detection
- 🧠 Sentiment analysis
- 🌐 Multi-language support
- ⚡ FastAPI backend
- 🖥️ Web dashboard for visualization

---

## 🎯 Use Cases

- News intelligence & monitoring
- Research & analysis
- Geopolitical trend tracking
- Semantic search applications
- NLP & ML portfolio project

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👤 Author

**Kajal**  
Machine Learning & AI Enthusiast

---

⭐ If you find this project useful, consider giving it a star!

