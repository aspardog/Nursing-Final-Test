"""
Database initialization and utilities for the quiz app.
"""
import os
import shutil
import sqlite3
from pathlib import Path

# Use /data/ for persistent storage on Hugging Face Spaces
IS_HF_SPACE = os.environ.get("SPACE_ID") is not None
LOCAL_DB_PATH = Path(__file__).parent / "data" / "quiz.db"
HF_DB_PATH = Path("/data/quiz.db")

if IS_HF_SPACE:
    DB_PATH = HF_DB_PATH
else:
    DB_PATH = LOCAL_DB_PATH


def ensure_db_exists():
    """Ensure database exists, copying from local if needed (for HF Spaces)."""
    if IS_HF_SPACE and not HF_DB_PATH.exists():
        HF_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        if LOCAL_DB_PATH.exists():
            shutil.copy(LOCAL_DB_PATH, HF_DB_PATH)
            print(f"Copied initial database to {HF_DB_PATH}")


def get_connection() -> sqlite3.Connection:
    """Get a connection to the SQLite database."""
    ensure_db_exists()
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database schema. Creates tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY,
            frente TEXT NOT NULL,
            dorso TEXT NOT NULL,
            tema TEXT NOT NULL,
            subtema TEXT,
            fuente TEXT,
            mcq_eligible BOOLEAN DEFAULT 1,
            explicacion TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("PRAGMA table_info(cards)")
    card_columns = {row[1] for row in cursor.fetchall()}
    if "explicacion" not in card_columns:
        cursor.execute("ALTER TABLE cards ADD COLUMN explicacion TEXT")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS distractors (
            id INTEGER PRIMARY KEY,
            card_id INTEGER NOT NULL REFERENCES cards(id),
            distractor_text TEXT NOT NULL,
            posicion INTEGER NOT NULL,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(card_id, posicion)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_sessions (
            id INTEGER PRIMARY KEY,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ended_at TIMESTAMP,
            n_questions INTEGER NOT NULL,
            n_correct INTEGER DEFAULT 0,
            temas TEXT,
            modo TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY,
            session_id INTEGER NOT NULL REFERENCES quiz_sessions(id),
            card_id INTEGER NOT NULL REFERENCES cards(id),
            formato TEXT NOT NULL,
            user_answer TEXT,
            correct BOOLEAN,
            self_evaluation TEXT,
            time_seconds INTEGER,
            answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
