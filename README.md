# SDA Satellite Link - Protocol and Coding Service

This service handles synchronization, channel coding (5G NR LDPC FEC), frame construction, scrambling, error control (CRC-16/CRC-32), and ARQ management. It exposes a FastAPI backend.

## Run locally

1. Create and configure environment:
   - Copy `.env.example` to `.env` and set variables as needed.
   - Allowed ports: `3000`, `3001`, `3002`, `5000`. Default for this service: `5000`.

2. Install dependencies:
   - Using pip
     - python -m venv .venv && . .venv/bin/activate
     - pip install -r ProtocolandCodingService/requirements.txt

3. Start the server:
   - From the service root directory:
     - cd ProtocolandCodingService
     - uvicorn main:app --host 0.0.0.0 --port 5000
     - Or override with env: `export PORT=5000 && uvicorn main:app --host 0.0.0.0 --port "${PORT}"`

Open Swagger UI at:
- http://localhost:5000/docs

The ASGI entrypoint `ProtocolandCodingService/main.py` re-exports the FastAPI instance from `src/api/main.py` as `app`. This ensures `uvicorn main:app` works reliably.

## Health check

- GET `/` returns `{ "message": "Healthy" }`.
- OpenAPI docs at `/docs`.

## Notes

- Do not hardcode secrets; use environment variables.
- To change ports, set `PORT` to one of: `3000`, `3001`, `3002`, `5000`. Any other value will be ignored and the service will default to `5000`.