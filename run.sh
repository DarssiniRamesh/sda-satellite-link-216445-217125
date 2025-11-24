#!/usr/bin/env bash
# Simple launcher for local development.
# If a virtualenv is used, ensure requirements are installed there before launching.

set -euo pipefail

PORT="${PORT:-3002}"
HOST="${HOST:-0.0.0.0}"

# Detect and activate virtual environment if present
if [ -n "${VIRTUAL_ENV:-}" ]; then
  echo "[run.sh] Using active virtualenv at ${VIRTUAL_ENV}"
elif [ -d ".venv" ]; then
  echo "[run.sh] Activating local .venv ..."
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

# Install requirements into current environment
if [ -f "requirements.txt" ]; then
  echo "[run.sh] Installing requirements ..."
  python -m pip install --upgrade pip
  python -m pip install --no-cache-dir -r requirements.txt
fi

echo "Starting ProtocolandCodingService on ${HOST}:${PORT} ..."
exec uvicorn main:app --host "${HOST}" --port "${PORT}" --reload
