#!/usr/bin/env bash
# Simple launcher for local development.
# Does not require activating a virtualenv; assumes uvicorn is available in the environment.

set -euo pipefail

PORT="${PORT:-3002}"
HOST="${HOST:-0.0.0.0}"

echo "Starting ProtocolandCodingService on ${HOST}:${PORT} ..."
exec uvicorn main:app --host "${HOST}" --port "${PORT}" --reload
