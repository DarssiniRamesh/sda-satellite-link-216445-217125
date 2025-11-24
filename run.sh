#!/usr/bin/env bash
# Simple launcher for local development.
# Ensures a venv exists, installs requirements, and launches uvicorn from the service root.

set -euo pipefail

# Move to the service root (directory containing main.py and ProtocolandCodingService/)
if [ -d "./ProtocolandCodingService" ] && [ -f "./main.py" ]; then
  : # already at service root
elif [ -d "./sda-satellite-link-216445-217125" ] && [ -f "./sda-satellite-link-216445-217125/main.py" ]; then
  cd "./sda-satellite-link-216445-217125"
elif [ -d "sda-satellite-link-216445-217125" ] && [ -f "sda-satellite-link-216445-217125/main.py" ]; then
  cd "sda-satellite-link-216445-217125"
fi

PORT="${PORT:-3002}"
HOST="${HOST:-0.0.0.0}"

# Create/activate virtual environment
VENV_DIR="${VENV_DIR:-.venv}"
if [ ! -d "${VENV_DIR}" ]; then
  echo "[run.sh] Creating local virtualenv at ${VENV_DIR} ..."
  python -m venv "${VENV_DIR}"
fi
# shellcheck disable=SC1090
source "${VENV_DIR}/bin/activate"

echo "[run.sh] Python: $(python --version 2>&1 || true)"
echo "[run.sh] Pip: $(python -m pip --version 2>&1 || true)"

# Always upgrade pip and install requirements
echo "[run.sh] Installing requirements ..."
python -m pip install --upgrade pip
if [ -f "requirements.txt" ]; then
  python -m pip install --no-cache-dir -r requirements.txt
fi

# Preflight import check. If it fails, attempt reinstall and fail if still missing.
if ! python -c "import fastapi, uvicorn" >/devnull 2>&1; then
  echo "[run.sh] fastapi/uvicorn not importable; attempting reinstall ..."
  if [ -f "requirements.txt" ]; then
    python -m pip install --no-cache-dir -r requirements.txt
  else
    python -m pip install --no-cache-dir 'fastapi>=0.110,<1.0' 'uvicorn[standard]>=0.24,<1.0'
  fi
  if ! python -c "import fastapi, uvicorn" >/dev/null 2>&1; then
    echo "[run.sh] ERROR: fastapi/uvicorn still not importable after reinstall. Aborting." >&2
    exit 1
  fi
fi

# Ensure we are in the service root so 'main:app' resolves
if [ ! -f "./main.py" ]; then
  echo "[run.sh] ERROR: main.py not found in current directory $(pwd). Aborting." >&2
  exit 1
fi

echo "[run.sh] Starting ProtocolandCodingService on ${HOST}:${PORT} from $(pwd) ..."
exec uvicorn main:app --host "${HOST}" --port "${PORT}" --reload
