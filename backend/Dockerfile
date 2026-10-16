# Use official lightweight Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install system build dependencies required for C-extensions and NLP libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements first to leverage Docker layer caching
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/backend/requirements.txt

# Download required NLP language models
RUN python -m spacy download en_core_web_sm || true

# Copy backend, AI engine, and test datasets into container
COPY ai_engine /app/ai_engine
COPY backend /app/backend
COPY data /app/data

# Create persistent storage directory for uploaded resumes
RUN mkdir -p /app/backend/uploads/resumes

EXPOSE 8000

# Run FastAPI backend with Uvicorn server
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
