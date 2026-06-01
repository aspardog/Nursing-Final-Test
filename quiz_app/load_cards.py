"""
Script to load cards from CSV files into the SQLite database.
"""
import re
from pathlib import Path
from database import get_connection, init_db
from text_normalizer import normalize_spanish_text

CARDS_DIR = Path(__file__).parent.parent / "cards"


def extract_fuente(dorso: str) -> str | None:
    """Extract the source (Fuente) from the card back."""
    match = re.search(r"Fuente:\s*([^<]+)", dorso)
    return match.group(1).strip() if match else None


def parse_tag(tag: str) -> tuple[str, str | None]:
    """
    Parse a hierarchical tag into tema and subtema.
    Example: 'examen_final::semiologia::atencion' -> ('semiologia', 'atencion')
    """
    partes = tag.split("::")
    tema = partes[1] if len(partes) > 1 else "general"
    subtema = partes[2] if len(partes) > 2 else None
    return tema, subtema


def is_mcq_eligible(dorso: str) -> bool:
    """
    Determine if a card is eligible for MCQ format.
    Returns False if:
    - Response has more than 30 words
    - Response is clearly an enumeration (multiple items with commas/semicolons)
    """
    # Remove HTML tags for word counting
    clean_text = re.sub(r"<[^>]+>", "", dorso)
    # Remove the source part
    clean_text = re.sub(r"Fuente:.*$", "", clean_text, flags=re.IGNORECASE)
    clean_text = clean_text.strip()

    words = clean_text.split()

    # Too long for MCQ
    if len(words) > 30:
        return False

    # Check for enumeration patterns (lists with many commas or semicolons)
    comma_count = clean_text.count(",")
    semicolon_count = clean_text.count(";")

    # If there are 4+ items separated by commas/semicolons, likely an enumeration
    if comma_count >= 4 or semicolon_count >= 3:
        return False

    return True


def load_csv(csv_path: Path) -> list[dict]:
    """
    Parse a CSV file with Anki format.
    Skips header lines starting with #.
    """
    cards = []

    with open(csv_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Skip empty lines and header lines
            if not line or line.startswith("#"):
                continue

            # Split by pipe
            parts = line.split("|")
            if len(parts) < 3:
                continue

            frente = parts[0].strip()
            dorso = parts[1].strip()
            tag = parts[2].strip()

            tema, subtema = parse_tag(tag)
            fuente = extract_fuente(dorso)
            mcq_eligible = is_mcq_eligible(dorso)

            cards.append({
                "frente": normalize_spanish_text(frente),
                "dorso": normalize_spanish_text(dorso),
                "tema": normalize_spanish_text(tema),
                "subtema": normalize_spanish_text(subtema),
                "fuente": normalize_spanish_text(fuente),
                "mcq_eligible": mcq_eligible
            })

    return cards


def load_cards_to_db(cards: list[dict]) -> int:
    """
    Load cards into the database.
    Idempotent: skips cards that already exist (by frente).
    Returns the number of cards inserted.
    """
    conn = get_connection()
    cursor = conn.cursor()

    inserted = 0
    for card in cards:
        # Check if card already exists
        cursor.execute("SELECT id FROM cards WHERE frente = ?", (card["frente"],))
        if cursor.fetchone():
            continue

        cursor.execute("""
            INSERT INTO cards (frente, dorso, tema, subtema, fuente, mcq_eligible)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            card["frente"],
            card["dorso"],
            card["tema"],
            card["subtema"],
            card["fuente"],
            card["mcq_eligible"]
        ))
        inserted += 1

    conn.commit()
    conn.close()
    return inserted


def main():
    # Initialize database
    init_db()

    # Find all CSV files in cards directory
    csv_files = list(CARDS_DIR.glob("*.csv"))

    if not csv_files:
        print(f"No CSV files found in {CARDS_DIR}")
        return

    total_loaded = 0
    for csv_file in csv_files:
        print(f"Processing {csv_file.name}...")
        cards = load_csv(csv_file)
        loaded = load_cards_to_db(cards)
        total_loaded += loaded
        print(f"  Loaded {loaded} new cards from {csv_file.name}")

    # Get total count from DB
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cards")
    total = cursor.fetchone()[0]
    conn.close()

    print(f"\n✅ Cargadas {total} tarjetas en quiz.db")


if __name__ == "__main__":
    main()
