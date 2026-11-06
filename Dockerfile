FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system dependencies once
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements for better Docker layer caching
COPY requirements.txt .

# Install CPU-only PyTorch first
RUN pip install --upgrade pip && \
    pip install torch --index-url https://download.pytorch.org/whl/cpu

# Install all remaining dependencies except standalone torch
RUN sed '/^[[:space:]]*torch[[:space:]]*$/Id' requirements.txt \
    > /tmp/requirements.txt && \
    pip install -r /tmp/requirements.txt

# Copy application source
COPY . .

# Create runtime directories
RUN mkdir -p \
    data/uploads \
    data/vectorstore \
    data/dataset \
    data/models \
    data/forecast_reports \
    logs

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
