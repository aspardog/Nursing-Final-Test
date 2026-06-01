"""
Quiz engine - handles question sampling and quiz generation.
"""
import random
import re
from database import get_connection


def clean_answer_for_display(dorso: str) -> str:
    """
    Clean the answer text for display.
    Removes HTML source tags but keeps other formatting.
    """
    # Remove the source part (usually at the end)
    clean = re.sub(r'<br><br><small><i>Fuente:.*?</i></small>', '', dorso)
    return clean.strip()


def get_answer_text(dorso: str) -> str:
    """
    Extract clean answer text without HTML for comparison.
    """
    clean = re.sub(r'<[^>]+>', '', dorso)
    clean = re.sub(r'Fuente:.*$', '', clean, flags=re.IGNORECASE)
    return clean.strip()


def get_available_temas() -> list[dict]:
    """
    Get list of available temas with card counts.
    Returns list of {tema, subtema, count, mcq_count}
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT tema, subtema,
               COUNT(*) as total,
               SUM(mcq_eligible) as mcq_eligible
        FROM cards
        GROUP BY tema, subtema
        ORDER BY tema, subtema
    """)

    results = []
    for row in cursor.fetchall():
        results.append({
            "tema": row[0],
            "subtema": row[1],
            "count": row[2],
            "mcq_count": row[3]
        })

    conn.close()
    return results


def sample_questions(
    n: int,
    temas: list[str] | None = None,
    subtemas: list[str] | None = None,
    modo: str = "mixto",
    ratio_mcq: float = 0.7
) -> list[dict]:
    """
    Sample questions for a quiz.

    Args:
        n: Number of questions to sample
        temas: Filter by tema(s), None for all
        subtemas: Filter by subtema(s), None for all
        modo: "mixto", "mcq", or "abierto"
        ratio_mcq: Ratio of MCQ questions (only for mixto mode)

    Returns:
        List of question dicts with format info
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Build query based on filters
    query = "SELECT id, frente, dorso, tema, subtema, mcq_eligible FROM cards WHERE 1=1"
    params = []

    if temas:
        placeholders = ",".join("?" * len(temas))
        query += f" AND tema IN ({placeholders})"
        params.extend(temas)

    if subtemas:
        placeholders = ",".join("?" * len(subtemas))
        query += f" AND subtema IN ({placeholders})"
        params.extend(subtemas)

    # For MCQ-only mode, only get eligible cards
    if modo == "mcq":
        query += " AND mcq_eligible = 1"

    cursor.execute(query, params)
    all_cards = [dict(row) for row in cursor.fetchall()]

    if not all_cards:
        conn.close()
        return []

    # Sample n cards (or all if less available)
    n = min(n, len(all_cards))
    sampled = random.sample(all_cards, n)

    # Determine format for each question
    questions = []

    if modo == "mcq":
        n_mcq = n
    elif modo == "abierto":
        n_mcq = 0
    else:  # mixto
        n_mcq = round(n * ratio_mcq)

    # Shuffle to randomize which cards get MCQ format
    random.shuffle(sampled)

    for i, card in enumerate(sampled):
        # Assign format: first n_mcq cards get MCQ if eligible
        if i < n_mcq and card["mcq_eligible"]:
            formato = "mcq"
        else:
            formato = "abierto"

        question = {
            "card_id": card["id"],
            "pregunta": card["frente"],
            "respuesta_correcta": clean_answer_for_display(card["dorso"]),
            "respuesta_texto": get_answer_text(card["dorso"]),
            "tema": card["tema"],
            "subtema": card["subtema"],
            "formato": formato
        }

        # Add options for MCQ
        if formato == "mcq":
            options = get_mcq_options(cursor, card["id"], card["dorso"])
            question["opciones"] = options["opciones"]
            question["respuesta_correcta_index"] = options["correcta_index"]

        questions.append(question)

    conn.close()

    # Shuffle final order
    random.shuffle(questions)

    return questions


def get_mcq_options(cursor, card_id: int, dorso: str) -> dict:
    """
    Get MCQ options for a card (correct answer + 3 distractors, shuffled).
    Returns dict with opciones list and correcta_index.
    """
    # Get distractors
    cursor.execute("""
        SELECT distractor_text FROM distractors
        WHERE card_id = ?
        ORDER BY posicion
    """, (card_id,))

    distractors = [row[0] for row in cursor.fetchall()]

    # Get correct answer (cleaned)
    correct = get_answer_text(dorso)

    # Combine and shuffle
    options = [correct] + distractors

    # Create list of (option, is_correct) tuples
    labeled = [(opt, i == 0) for i, opt in enumerate(options)]
    random.shuffle(labeled)

    # Find correct index after shuffle
    opciones = [opt for opt, _ in labeled]
    correcta_index = next(i for i, (_, is_correct) in enumerate(labeled) if is_correct)

    return {
        "opciones": opciones,
        "correcta_index": correcta_index
    }


def create_session(n_questions: int, temas: str | None, modo: str) -> int:
    """
    Create a new quiz session in the database.
    Returns session_id.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO quiz_sessions (n_questions, temas, modo)
        VALUES (?, ?, ?)
    """, (n_questions, temas, modo))

    session_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return session_id


def record_response(
    session_id: int,
    card_id: int,
    formato: str,
    user_answer: str | None,
    correct: bool | None,
    self_evaluation: str | None = None,
    time_seconds: int | None = None
):
    """Record a user's response to a question."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO responses (session_id, card_id, formato, user_answer, correct, self_evaluation, time_seconds)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (session_id, card_id, formato, user_answer, correct, self_evaluation, time_seconds))

    # Update session correct count if applicable
    if correct:
        cursor.execute("""
            UPDATE quiz_sessions
            SET n_correct = n_correct + 1
            WHERE id = ?
        """, (session_id,))

    conn.commit()
    conn.close()


def end_session(session_id: int):
    """Mark a session as ended."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE quiz_sessions
        SET ended_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (session_id,))

    conn.commit()
    conn.close()


def get_session_summary(session_id: int) -> dict:
    """Get summary statistics for a completed session."""
    conn = get_connection()
    cursor = conn.cursor()

    # Get session info
    cursor.execute("""
        SELECT id, started_at, ended_at, n_questions, n_correct, temas, modo
        FROM quiz_sessions WHERE id = ?
    """, (session_id,))

    session = cursor.fetchone()
    if not session:
        conn.close()
        return None

    # Get responses with card info
    cursor.execute("""
        SELECT r.card_id, r.formato, r.correct, r.self_evaluation, r.time_seconds,
               c.frente, c.subtema, c.dorso
        FROM responses r
        JOIN cards c ON r.card_id = c.id
        WHERE r.session_id = ?
        ORDER BY r.answered_at
    """, (session_id,))

    responses = []
    by_subtema = {}
    by_formato = {"mcq": {"total": 0, "correct": 0}, "abierto": {"total": 0, "correct": 0}}
    failed_cards = []

    for row in cursor.fetchall():
        resp = {
            "card_id": row[0],
            "formato": row[1],
            "correct": row[2],
            "self_evaluation": row[3],
            "time_seconds": row[4],
            "pregunta": row[5],
            "subtema": row[6],
            "respuesta_correcta": clean_answer_for_display(row[7])
        }
        responses.append(resp)

        # Aggregate by subtema
        subtema = row[6]
        if subtema not in by_subtema:
            by_subtema[subtema] = {"total": 0, "correct": 0}
        by_subtema[subtema]["total"] += 1

        # Determine if correct (MCQ: correct field, Abierto: self_evaluation)
        is_correct = row[2] if row[1] == "mcq" else (row[3] == "sabia")
        if is_correct:
            by_subtema[subtema]["correct"] += 1
        else:
            failed_cards.append({
                "card_id": row[0],
                "pregunta": row[5],
                "subtema": row[6],
                "respuesta_correcta": clean_answer_for_display(row[7])
            })

        # Aggregate by formato
        by_formato[row[1]]["total"] += 1
        if is_correct:
            by_formato[row[1]]["correct"] += 1

    conn.close()

    return {
        "session_id": session[0],
        "started_at": session[1],
        "ended_at": session[2],
        "n_questions": session[3],
        "n_correct": session[4],
        "temas": session[5],
        "modo": session[6],
        "responses": responses,
        "by_subtema": by_subtema,
        "by_formato": by_formato,
        "failed_cards": failed_cards
    }


def get_session_history(limit: int = 20) -> list[dict]:
    """Get recent quiz sessions."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, started_at, ended_at, n_questions, n_correct, temas, modo
        FROM quiz_sessions
        ORDER BY started_at DESC
        LIMIT ?
    """, (limit,))

    sessions = []
    for row in cursor.fetchall():
        sessions.append({
            "session_id": row[0],
            "started_at": row[1],
            "ended_at": row[2],
            "n_questions": row[3],
            "n_correct": row[4],
            "temas": row[5],
            "modo": row[6],
            "score_percent": round(row[4] / row[3] * 100) if row[3] > 0 else 0
        })

    conn.close()
    return sessions
