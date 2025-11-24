#!/usr/bin/env bash
# Simple launcher for local development.
# Ensures a venv exists, installs requirements, and launches uvicorn from the service root.

set -euo pipefail

# Standardize working directory to service root (folder containing main.py and requirements.txt)
if [ -d "./ProtocolandCodingService" ] && [ -f "./main.py" ]; then
  : # already at service root
elif [ -d "./sda-satellite-link-216445-217125" ]; then
  cd "./sda-satellite-link-216445-217125"
elif [ -d "sda-satellite-link-216445-217125" ]; then
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

# Install requirements unconditionally to avoid missing fastapi issues
if [ -f "requirements.txt" ]; then
  echo "[run.sh] Installing requirements ..."
  python -m pip install --upgrade pip
  python -m pip install --no-cache-dir -r requirements.txt
fi

# Quick import check and remediate if necessary
if ! python -c "import fastapi, uvicorn" >/dev/null 2>&1; then
  echo "[run.sh] fastapi/uvicorn not importable; reinstalling ..."
  if [ -f "requirements.txt" ]; then
    python -m pip install --no-cache-dir -r requirements.txt
  else
    python -m pip install --no-cache-dir fastapi uvicorn[standard]
  fi
fi

echo "[run.sh] Starting ProtocolandCodingService on ${HOST}:${PORT} from $(pwd) ..."
# Ensure we always run from the service root and use main:app
exec uvicorn main:app --host "${HOST}" --port "${PORT}" --reload
