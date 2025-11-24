FROM python:3.11-slim

# Use /app as the container workspace and service root containing main.py
WORKDIR /app

# Install system dependencies useful for building dependencies
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency file and install once at build time for faster container start
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

# Copy application source into /app (service root holds main.py and ProtocolandCodingService/)
COPY . /app

# Ensure bootstrap is executable
RUN chmod +x /app/bootstrap.sh

# Expose service port
EXPOSE 3002

# Environment
ENV PORT=3002 HOST=0.0.0.0

# Standardized entrypoint: bootstrap will ensure venv and install requirements, then run uvicorn main:app
ENTRYPOINT ["/app/bootstrap.sh"]
