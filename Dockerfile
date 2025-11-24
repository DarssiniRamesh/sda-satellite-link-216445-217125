FROM python:3.11-slim

WORKDIR /app

# Install system dependencies useful for building dependencies
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application source
COPY . /app

# Expose service port
EXPOSE 3002

# Environment
ENV PORT=3002 HOST=0.0.0.0

# Run FastAPI via uvicorn targeting the root entrypoint (main:app)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3002"]
