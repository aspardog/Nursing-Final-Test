"""
Database initialization and utilities for the quiz app.
"""
import os
import shutil
import sqlite3
from pathlib import Path

# Version number - increment this to force database rebuild on HF Spaces
DB_VERSION = 4  # v4: validate persisted DB contains all 4 main topics
EXPECTED_TEMAS = {"salud_mental", "urgencias", "cirugia", "mezclas"}
EXPECTED_MIN_CARDS = 354

# Use /data/ for persistent storage on Hugging Face Spaces
IS_HF_SPACE = os.environ.get("SPACE_ID") is not None
LOCAL_DB_PATH = Path(__file__).parent / "data" / "quiz.db"
HF_DB_PATH = Path("/data/quiz.db")
HF_VERSION_PATH = Path("/data/db_version.txt")

if IS_HF_SPACE:
    DB_PATH = HF_DB_PATH
else:
    DB_PATH = LOCAL_DB_PATH


def get_stored_version() -> int:
    """Get the stored database version on HF Spaces."""
    if HF_VERSION_PATH.exists():
        try:
            return int(HF_VERSION_PATH.read_text().strip())
        except (ValueError, IOError):
            return 0
    return 0


def set_stored_version(version: int):
    """Store the database version on HF Spaces."""
    HF_VERSION_PATH.parent.mkdir(parents=True, exist_ok=True)
    HF_VERSION_PATH.write_text(str(version))


def hf_db_has_expected_content() -> bool:
    """Check that the persisted HF database has the expected card dataset."""
    if not HF_DB_PATH.exists():
        return False

    try:
        conn = sqlite3.connect(HF_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cards")
        card_count = cursor.fetchone()[0]
        cursor.execute("SELECT DISTINCT tema FROM cards")
        temas = {row[0] for row in cursor.fetchall()}
        conn.close()
    except sqlite3.Error:
        return False

    return card_count >= EXPECTED_MIN_CARDS and EXPECTED_TEMAS.issubset(temas)


def ensure_db_exists():
    """Ensure database exists, copying from local if needed (for HF Spaces)."""
    if IS_HF_SPACE:
        stored_version = get_stored_version()
        needs_update = (
            stored_version < DB_VERSION
            or not hf_db_has_expected_content()
        )

        if needs_update and LOCAL_DB_PATH.exists():
            HF_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(LOCAL_DB_PATH, HF_DB_PATH)
            set_stored_version(DB_VERSION)
            print(f"Updated database to version {DB_VERSION} at {HF_DB_PATH}")


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
