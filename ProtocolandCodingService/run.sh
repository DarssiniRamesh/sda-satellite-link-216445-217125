#!/usr/bin/env bash
set -euo pipefail

# This script installs dependencies (without relying on an existing virtual environment)
# and runs the Protocol and Coding Service using uvicorn.
# Defaults: HOST=0.0.0.0, PORT=3002 (override with environment variables)

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

# Upgrade pip and install requirements
echo "[INFO] Installing dependencies..."
$PIP install --upgrade pip >/dev/null
$PIP install -r "${APP_DIR}/requirements.txt"

# Export PORT with default 3002 if not set
export PORT="${PORT:-3002}"
export HOST="${HOST:-0.0.0.0}"

echo "[INFO] Starting uvicorn app at app.main:app on ${HOST}:${PORT}"
exec uvicorn app.main:app --host "${HOST}" --port "${PORT}"
