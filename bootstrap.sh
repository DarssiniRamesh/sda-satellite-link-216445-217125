#!/usr/bin/env bash
# Bootstrap script for ProtocolandCodingService to ensure dependencies are installed
# and start the FastAPI app with uvicorn.

set -euo pipefail

# Move to the service root (directory containing main.py and ProtocolandCodingService/)
if [ -d "/app/ProtocolandCodingService" ] && [ -f "/app/main.py" ]; then
  cd /app
elif [ -f "./main.py" ] && [ -d "./ProtocolandCodingService" ]; then
  : # already at service root
elif [ -d "./sda-satellite-link-216445-217125" ] && [ -f "./sda-satellite-link-216445-217125/main.py" ]; then
  cd ./sda-satellite-link-216445-217125
else
  # best-effort: if a nested directory exists, move into it
  for d in sda-satellite-link-216445-217125 .; do
    if [ -d "$d" ] && [ -f "$d/main.py" ] && [ -d "$d/ProtocolandCodingService" ]; then
      cd "$d"
      break
    fi
  done
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

# Always upgrade pip and install dependencies
REQ_FILE="requirements.txt"
if [ -f "/app/requirements.txt" ]; then
  REQ_FILE="/app/requirements.txt"
elif [ ! -f "${REQ_FILE}" ]; then
  echo "[bootstrap] WARNING: requirements.txt not found; proceeding but startup may fail."
fi

echo "[bootstrap] Installing dependencies ..."
python -m pip install --upgrade pip
if [ -f "${REQ_FILE}" ]; then
  python -m pip install --no-cache-dir -r "${REQ_FILE}"
fi

# Preflight import check. If it fails, attempt reinstall once and fail with clear message if still missing.
if ! python -c "import fastapi, uvicorn" >/dev/null 2>&1; then
  echo "[bootstrap] fastapi/uvicorn not importable; attempting reinstall ..."
  if [ -f "${REQ_FILE}" ]; then
    python -m pip install --no-cache-dir -r "${REQ_FILE}"
  else
    python -m pip install --no-cache-dir 'fastapi>=0.110,<1.0' 'uvicorn[standard]>=0.24,<1.0'
  fi
  if ! python -c "import fastapi, uvicorn" >/dev/null 2>&1; then
    echo "[bootstrap] ERROR: fastapi/uvicorn still not importable after reinstall. Aborting." >&2
    exit 1
  fi
fi

# Ensure we are in the service root so 'main:app' resolves
if [ ! -f "./main.py" ]; then
  echo "[bootstrap] ERROR: main.py not found in current directory $(pwd). Aborting." >&2
  exit 1
fi

echo "[bootstrap] Launching uvicorn main:app on ${HOST}:${PORT} from $(pwd) ..."
exec uvicorn main:app --host "${HOST}" --port "${PORT}"
