# ProtocolandCodingService

Minimal FastAPI scaffolding providing health and root endpoints.

## Endpoints
- GET `/` — service metadata
- GET `/health` — health probe

## Run locally
```bash
pip install -r requirements.txt

# Option 1: Use the top-level ASGI entrypoint (recommended, matches orchestrator)
uvicorn main:app --host 0.0.0.0 --port "${PORT:-8000}"

# Option 2: Directly reference the module path
uvicorn src.api.main:app --host 0.0.0.0 --port "${PORT:-8000}"
```
