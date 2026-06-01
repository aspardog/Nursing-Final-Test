"""
FastAPI application for the quiz app.
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path

from database import init_db
from quiz_engine import (
    get_available_temas,
    sample_questions,
    create_session,
    record_response,
    end_session,
    get_session_summary,
    get_session_history
)

# Initialize database on startup
init_db()

app = FastAPI(title="Quiz App - Enfermería")

# Mount static files
STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# --- Pydantic Models ---

class QuizStartRequest(BaseModel):
    n_questions: int = 10
    temas: list[str] | None = None
    subtemas: list[str] | None = None
    modo: str = "mixto"  # mixto, mcq, abierto
    ratio_mcq: float = 0.7


class AnswerRequest(BaseModel):
    session_id: int
    card_id: int
    formato: str
    user_answer: str | None = None
    correct: bool | None = None  # For MCQ
    self_evaluation: str | None = None  # For abierto: "sabia", "medias", "no_sabia"
    time_seconds: int | None = None


class EndSessionRequest(BaseModel):
    session_id: int


# --- Routes ---

@app.get("/")
async def index():
    """Serve the main index.html"""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "API del quiz de enfermería. El frontend aún no está construido."}


@app.get("/api/temas")
async def list_temas():
    """Get available temas/subtemas with card counts."""
    temas = get_available_temas()
    return {"temas": temas}


@app.post("/api/quiz/start")
async def start_quiz(request: QuizStartRequest):
    """
    Start a new quiz session.
    Returns session_id and list of questions.
    """
    # Validate modo
    if request.modo not in ["mixto", "mcq", "abierto"]:
        raise HTTPException(status_code=400, detail="El modo debe ser mixto, mcq o abierto.")

    # Validate n_questions
    if request.n_questions < 1 or request.n_questions > 100:
        raise HTTPException(status_code=400, detail="n_questions debe estar entre 1 y 100.")

    # Sample questions
    questions = sample_questions(
        n=request.n_questions,
        temas=request.temas,
        subtemas=request.subtemas,
        modo=request.modo,
        ratio_mcq=request.ratio_mcq
    )

    if not questions:
        raise HTTPException(status_code=404, detail="No se encontraron tarjetas con los filtros seleccionados.")

    # Create session
    temas_str = ",".join(request.temas) if request.temas else None
    session_id = create_session(
        n_questions=len(questions),
        temas=temas_str,
        modo=request.modo
    )

    return {
        "session_id": session_id,
        "n_questions": len(questions),
        "questions": questions
    }


@app.post("/api/quiz/answer")
async def submit_answer(request: AnswerRequest):
    """Submit an answer for a question."""
    record_response(
        session_id=request.session_id,
        card_id=request.card_id,
        formato=request.formato,
        user_answer=request.user_answer,
        correct=request.correct,
        self_evaluation=request.self_evaluation,
        time_seconds=request.time_seconds
    )

    return {"status": "recorded"}


@app.post("/api/quiz/end")
async def finish_quiz(request: EndSessionRequest):
    """End a quiz session and get summary."""
    end_session(request.session_id)
    summary = get_session_summary(request.session_id)

    if not summary:
        raise HTTPException(status_code=404, detail="Sesión no encontrada.")

    return summary


@app.get("/api/quiz/{session_id}/summary")
async def quiz_summary(session_id: int):
    """Get summary for a specific session."""
    summary = get_session_summary(session_id)

    if not summary:
        raise HTTPException(status_code=404, detail="Sesión no encontrada.")

    return summary


@app.get("/api/history")
async def history(limit: int = 20):
    """Get recent quiz sessions."""
    sessions = get_session_history(limit=limit)
    return {"sessions": sessions}


# For running with: python app.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
