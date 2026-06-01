"""
Distractor generator for MCQ questions.
This script generates plausible but incorrect answer options for multiple choice questions.

The distractors are pre-generated and cached in the database.
"""
import re
from database import get_connection


def clean_answer(dorso: str) -> str:
    """Remove HTML tags and source info from answer."""
    # Remove HTML tags
    clean = re.sub(r"<[^>]+>", "", dorso)
    # Remove source
    clean = re.sub(r"Fuente:.*$", "", clean, flags=re.IGNORECASE)
    return clean.strip()


def get_cards_without_distractors(limit: int | None = None) -> list[dict]:
    """Get cards that are MCQ eligible but don't have distractors yet."""
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT c.id, c.frente, c.dorso, c.subtema
        FROM cards c
        WHERE c.mcq_eligible = 1
        AND c.id NOT IN (SELECT DISTINCT card_id FROM distractors)
    """
    if limit:
        query += f" LIMIT {limit}"

    cursor.execute(query)
    cards = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return cards


def insert_distractors(card_id: int, distractors: list[str]):
    """Insert distractors for a card."""
    conn = get_connection()
    cursor = conn.cursor()

    for i, distractor in enumerate(distractors):
        cursor.execute("""
            INSERT OR REPLACE INTO distractors (card_id, distractor_text, posicion)
            VALUES (?, ?, ?)
        """, (card_id, distractor, i + 1))

    conn.commit()
    conn.close()


def get_distractors_for_card(card_id: int) -> list[str]:
    """Get existing distractors for a card."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT distractor_text FROM distractors
        WHERE card_id = ?
        ORDER BY posicion
    """, (card_id,))

    distractors = [row[0] for row in cursor.fetchall()]
    conn.close()
    return distractors


def show_pilot_cards():
    """Show pilot cards with their distractors for review."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.id, c.frente, c.dorso, c.subtema,
               GROUP_CONCAT(d.distractor_text, '|||') as distractors
        FROM cards c
        JOIN distractors d ON c.id = d.card_id
        GROUP BY c.id
        ORDER BY c.subtema
        LIMIT 10
    """)

    results = cursor.fetchall()
    conn.close()

    for row in results:
        print(f"\n{'='*60}")
        print(f"ID: {row[0]} | Subtema: {row[3]}")
        print(f"Pregunta: {row[1]}")
        clean = clean_answer(row[2])
        print(f"Respuesta correcta: {clean}")
        print("Distractoras:")
        for i, d in enumerate(row[4].split("|||"), 1):
            print(f"  {i}. {d}")

    return results


if __name__ == "__main__":
    # Show stats
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM cards WHERE mcq_eligible = 1")
    total_eligible = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT card_id) FROM distractors")
    with_distractors = cursor.fetchone()[0]

    conn.close()

    print(f"Tarjetas MCQ elegibles: {total_eligible}")
    print(f"Con distractoras: {with_distractors}")
    print(f"Pendientes: {total_eligible - with_distractors}")
