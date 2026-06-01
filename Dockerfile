FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.5.31 /uv /uvx /bin/

# Copy dependency metadata first for better caching.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application code
COPY quiz_app/ ./quiz_app/
COPY cards/ ./cards/

# Initialize database with cards
WORKDIR /app/quiz_app
RUN uv run --frozen python load_cards.py
RUN uv run --frozen python generate_explanations.py

# Expose port (7860 for Hugging Face Spaces)
EXPOSE 7860

# Run the application
CMD ["sh", "-c", "uv run --frozen python -m uvicorn app:app --host 0.0.0.0 --port ${PORT:-7860}"]
