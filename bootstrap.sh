#!/usr/bin/env bash
# Bootstrap script for ProtocolandCodingService to ensure dependencies are installed
# and start the FastAPI app with uvicorn.

set -euo pipefail

# Standardize working directory to the service root where main.py lives
# Container copies code into /app, so prefer that; otherwise fallback relative.
if [ -d "/app/ProtocolandCodingService" ]; then
  cd /app || true
elif [ -f "./main.py" ] && [ -d "./ProtocolandCodingService" ]; then
  # already at service root
  :
else
  # Try to locate the service folder relative to current working directory
  if [ -d "./sda-satellite-link-216445-217125" ]; then
    cd ./sda-satellite-link-216445-217125 || true
  fi
fi

# Use provided HOST/PORT env vars or defaults
PORT="${PORT:-3002}"
HOST="${HOST:-0.0.0.0}"

# Ensure a virtual environment exists and activate it
VENV_DIR="${VENV_DIR:-.venv}"
if [ ! -d "${VENV_DIR}" ]; then
  echo "[bootstrap] Creating virtual environment at ${VENV_DIR} ..."
  python -m venv "${VENV_DIR}"
fi
# shellcheck disable=SC1090
source "${VENV_DIR}/bin/activate"

echo "[bootstrap] Python version: $(python --version 2>&1 || true)"
echo "[bootstrap] Pip version: $(python -m pip --version 2>&1 || true)"

# Always install requirements to ensure fastapi is present, especially on fresh environments or bind mounts
REQ_FILE="requirements.txt"
if [ -f "/app/requirements.txt" ]; then
  REQ_FILE="/app/requirements.txt"
elif [ ! -f "${REQ_FILE}" ]; then
  echo "[bootstrap] WARNING: requirements.txt not found; proceeding but startup may fail."
fi

if [ -f "${REQ_FILE}" ]; then
  echo "[bootstrap] Installing dependencies from ${REQ_FILE} ..."
  python -m pip install --upgrade pip
  python -m pip install --no-cache-dir -r "${REQ_FILE}"
fi

# Quick import check to fail early and attempt reinstall if needed
if ! python -c "import fastapi, uvicorn" >/dev/null 2>&1; then
  echo "[bootstrap] fastapi/uvicorn not importable; retrying pip install ..."
  if [ -f "${REQ_FILE}" ]; then
    python -m pip install --no-cache-dir -r "${REQ_FILE}"
  else
    python -m pip install --no-cache-dir fastapi uvicorn[standard]
  fi
  # Recheck and fail loudly if still missing
  if ! python -c "import fastapi, uvicorn" >/dev/null 2>&1; then
    echo "[bootstrap] ERROR: fastapi still not importable after install. Aborting." >&2
    exit 1
  fi
fi

echo "[bootstrap] Launching uvicorn main:app on ${HOST}:${PORT} from $(pwd) ..."
# Do not use 'ProtocolandCodingService.app.main' path; always use plain main:app from service root.
exec uvicorn main:app --host "${HOST}" --port "${PORT}"
