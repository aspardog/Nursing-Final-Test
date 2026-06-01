"""
Entry point for Hugging Face Spaces.
"""
import sys
from pathlib import Path

# Add quiz_app to path
quiz_app_path = Path(__file__).parent / "quiz_app"
sys.path.insert(0, str(quiz_app_path))

# Change working directory to quiz_app for relative imports
import os
os.chdir(quiz_app_path)

# Initialize database and load data if needed
from database import init_db, get_connection
from pathlib import Path as P

init_db()

# Check if cards are loaded, if not load them
conn = get_connection()
cursor = conn.execute("SELECT COUNT(*) FROM cards")
count = cursor.fetchone()[0]
conn.close()

if count == 0:
    print("Loading cards into database...")
    from load_cards import load_cards_from_csv
    csv_path = quiz_app_path / "data" / "anki_cards.csv"
    if csv_path.exists():
        load_cards_from_csv(str(csv_path))
        print("Cards loaded successfully!")
    else:
        print(f"Warning: CSV file not found at {csv_path}")

# Import the FastAPI app
from app import app

# For Hugging Face Spaces
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
