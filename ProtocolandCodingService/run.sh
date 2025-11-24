#!/usr/bin/env bash
# Robust start script for ProtocolandCodingService
# - Installs dependencies
# - Starts uvicorn with env-configurable HOST/PORT (defaults HOST=0.0.0.0, PORT=3002)
# - Handles SIGINT/SIGTERM gracefully so orchestrator stop does not appear as failure

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="${SCRIPT_DIR}"

# Detect Python/pip
if command -v python3 >/dev/null 2>&1; then
  PY=python3
else
  PY=python
fi

if command -v pip3 >/dev/null 2>&1; then
  PIP=pip3
else
  PIP=pip
fi

echo "[INFO] Using Python: $($PY -V 2>&1 || echo python not found)"
echo "[INFO] Using Pip: $($PIP -V 2>&1 || echo pip not found)"

# Upgrade pip and install requirements quietly for CI stability
echo "[INFO] Installing dependencies..."
$PIP install --upgrade pip -q
$PIP install -q -r "${APP_DIR}/requirements.txt"

# Defaults
export PORT="${PORT:-3002}"
export HOST="${HOST:-0.0.0.0}"

echo "[INFO] Starting uvicorn app at app.main:app on ${HOST}:${PORT}"

# Forward signals and treat common termination codes as success
_term() {
  echo "[INFO] Caught termination signal, forwarding to uvicorn (PID=${UVICORN_PID})"
  kill -TERM "${UVICORN_PID}" 2>/dev/null || true
}

_int() {
  echo "[INFO] Caught interrupt signal, forwarding to uvicorn (PID=${UVICORN_PID})"
  kill -INT "${UVICORN_PID}" 2>/dev/null || true
}

# Start uvicorn in background to allow trapping
uvicorn app.main:app --host "${HOST}" --port "${PORT}" &
UVICORN_PID=$!

trap _term TERM
trap _int INT

# Wait for uvicorn and capture exit code
wait "${UVICORN_PID}"
UVICORN_EXIT=$?

# Map signal-related exit codes to success (0):
# 130 = SIGINT, 143 = SIGTERM
if [ "${UVICORN_EXIT}" -eq 0 ] || [ "${UVICORN_EXIT}" -eq 130 ] || [ "${UVICORN_EXIT}" -eq 143 ]; then
  echo "[INFO] Uvicorn exited cleanly with code ${UVICORN_EXIT}"
  exit 0
fi

echo "[ERROR] Uvicorn exited with code ${UVICORN_EXIT}"
exit "${UVICORN_EXIT}"
