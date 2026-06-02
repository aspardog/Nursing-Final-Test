"""
Script to load cards from CSV files into the SQLite database.
"""
import re
from pathlib import Path
from database import get_connection, init_db
from text_normalizer import normalize_spanish_text

CARDS_DIR = Path(__file__).parent.parent / "cards"

# Orden determinista de carga para IDs predecibles
# Importante: no cambiar el orden sin actualizar generate_distractors.py y generate_explanations.py
CSV_ORDER = [
    "cards_semiologia.csv",       # IDs 1-209
    "cards_urgencias_basic.csv",  # IDs 210-261
    "cards_salas_basic.csv",      # IDs 262-295
    "cards_arritmias_basic.csv",  # IDs 296-312
    "cards_mezclas_basic.csv",    # IDs 313-326
    "cards_semiologia_cloze.csv", # IDs 327-331
    "cards_urgencias_cloze.csv",  # IDs 332-346
    "cards_salas_cloze.csv",      # IDs 347-352
    "cards_arritmias_cloze.csv",  # ID 353
    "cards_mezclas_cloze.csv",    # ID 354
]


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


def is_mcq_eligible(dorso: str, note_type: str = "Basic") -> bool:
    """
    Determine if a card is eligible for MCQ format.
    Returns False if:
    - Card is Cloze type (designed for fill-in-the-blank, not MCQ)
    - Response has more than 30 words
    - Response is clearly an enumeration (multiple items with commas/semicolons)
    """
    # Cloze cards are not MCQ eligible - they use {{c1::...}} format
    if note_type == "Cloze":
        return False

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
    Detects note type (Basic/Cloze) from header.
    """
    cards = []
    note_type = "Basic"  # Default

    with open(csv_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Parse header lines to detect note type
            if line.startswith("#"):
                if line.startswith("#notetype:"):
                    note_type = line.split(":")[1].strip()
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
            mcq_eligible = is_mcq_eligible(dorso, note_type)

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

    # Use deterministic order for predictable card IDs
    csv_files = []
    for csv_name in CSV_ORDER:
        csv_path = CARDS_DIR / csv_name
        if csv_path.exists():
            csv_files.append(csv_path)
        else:
            print(f"⚠️  Warning: {csv_name} not found, skipping")

    # Also load any CSV files not in CSV_ORDER (for future additions)
    for csv_path in CARDS_DIR.glob("*.csv"):
        if csv_path.name not in CSV_ORDER:
            print(f"⚠️  Warning: {csv_path.name} not in CSV_ORDER, loading at end")
            csv_files.append(csv_path)

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

    # Get total count and MCQ eligible count from DB
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cards")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM cards WHERE mcq_eligible = 1")
    mcq_count = cursor.fetchone()[0]
    conn.close()

    print(f"\n✅ Cargadas {total} tarjetas en quiz.db ({mcq_count} elegibles para MCQ)")


if __name__ == "__main__":
    main()
