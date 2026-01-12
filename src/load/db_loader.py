# db_loader.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import sys

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()  # automatically loads .env in the project root

# Required environment variables
REQUIRED_VARS = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]

# Check all required variables are set
missing_vars = [var for var in REQUIRED_VARS if not os.getenv(var)]
if missing_vars:
    print(f"[ERROR] Missing required environment variables: {', '.join(missing_vars)}")
    sys.exit(1)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# -----------------------------
# Database connection
# -----------------------------
def create_db_engine():
    """Create a SQLAlchemy engine for PostgreSQL."""
    try:
        db_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(db_url)
        # Test the connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("[SUCCESS] Connected to PostgreSQL database!")
        return engine
    except SQLAlchemyError as e:
        print(f"[ERROR] Could not connect to the database: {e}")
        sys.exit(1)

# -----------------------------
# Example data loader function
# -----------------------------
def load_sample_data(engine):
    """
    Example function to load data into the database.
    Replace this with your actual ETL logic.
    """
    try:
        with engine.begin() as conn:  # automatic commit/rollback
            conn.execute(text("CREATE TABLE IF NOT EXISTS sample_table (id SERIAL PRIMARY KEY, name TEXT);"))
            conn.execute(text("INSERT INTO sample_table (name) VALUES ('Hello World');"))
        print("[SUCCESS] Sample data loaded successfully!")
    except SQLAlchemyError as e:
        print(f"[ERROR] Failed to load data: {e}")

# -----------------------------
# Main execution
# -----------------------------
if __name__ == "__main__":
    engine = create_db_engine()
    # Call your data loading functions here
    load_sample_data(engine)
