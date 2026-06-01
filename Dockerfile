FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY quiz_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY quiz_app/ ./quiz_app/
COPY cards/ ./cards/

# Initialize database with cards
WORKDIR /app/quiz_app
RUN python load_cards.py
RUN python generate_explanations.py

# Expose port (7860 for Hugging Face Spaces)
EXPOSE 7860

# Run the application
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
