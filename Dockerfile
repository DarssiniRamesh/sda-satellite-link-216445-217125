# Python base image
FROM python:3.11-slim

# Install system dependencies (optional but useful)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application source
COPY . /app

# Expose the service port
EXPOSE 3002

# Default environment (can be overridden)
ENV PORT=3002
ENV HOST=0.0.0.0

# Start using uvicorn from the repository root entrypoint
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3002"]
```

Explanation: Ignore build artifacts in Docker context
````write file="sda-satellite-link-216445-217125/.dockerignore"
__pycache__/
*.pyc
*.pyo
*.pyd
*.pytest_cache/
*.coverage
dist/
build/
.env
.git
.gitignore
README.md
