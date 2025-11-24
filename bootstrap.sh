#!/usr/bin/env bash
# Bootstrap script for ProtocolandCodingService to ensure dependencies are installed
# and start the FastAPI app with uvicorn.

set -euo pipefail

# Use provided HOST/PORT env vars or defaults
PORT="${PORT:-3002}"
HOST="${HOST:-0.0.0.0}"

echo "[bootstrap] Python version: $(python --version 2>&1 || true)"
echo "[bootstrap] Pip version: $(python -m pip --version 2>&1 || true)"

# Install dependencies if requirements.txt exists
if [ -f "/app/requirements.txt" ]; then
  echo "[bootstrap] Installing dependencies from /app/requirements.txt ..."
  python -m pip install --no-cache-dir -r /app/requirements.txt
else
  if [ -f "requirements.txt" ]; then
    echo "[bootstrap] Installing dependencies from requirements.txt ..."
    python -m pip install --no-cache-dir -r requirements.txt
  else
    echo "[bootstrap] WARNING: requirements.txt not found; attempting to proceed."
  fi
fi

echo "[bootstrap] Launching uvicorn main:app on ${HOST}:${PORT} ..."
exec uvicorn main:app --host "${HOST}" --port "${PORT}"
