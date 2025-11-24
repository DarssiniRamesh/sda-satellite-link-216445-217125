# Protocol and Coding Service

FastAPI backend for protocol processing and coding functions in the SDA Satellite Link project.

## Features
- Root `main.py` entrypoint so you can run from the repo container root:
  - `uvicorn main:app --reload --port 3002`
- Health and version endpoints:
  - `GET /health` → `{ "status": "ok", "service": "Protocol and Coding Service" }`
  - `GET /version` → `{ "name": "Protocol and Coding Service", "version": "0.1.0" }`
- Pydantic settings with `.env` support and defaults
- Basic logging configuration
- Dockerfile for containerized runs

## Quickstart

### 1) Install dependencies
```
python -m pip install -r requirements.txt
```

### 2) Run locally
From the repository container root (`sda-satellite-link-216445-217125`):
```
uvicorn main:app --reload --port 3002
```

From inside the service package directory (`sda-satellite-link-216445-217125/ProtocolandCodingService`):
```
uvicorn main:app --reload --port 3002
```

Or use the helper script:
```
bash run.sh
```

### 3) Environment configuration
Copy `.env.example` to `.env` and edit as needed:
```
cp .env.example .env
```

Available variables:
- `HOST` (default: `0.0.0.0`)
- `PORT` (default: `3002`)
- `APP_NAME`, `APP_DESCRIPTION`, `APP_VERSION`
- `DEBUG` (default: `false`)

### 4) Docker
Build and run:
```
docker build -t protocol-coding-service .
docker run --rm -p 3002:3002 protocol-coding-service
```

The service will be available at:
- http://localhost:3002/health
- http://localhost:3002/version
- http://localhost:3002/docs

## Notes
- This scaffolding is non-destructive and does not remove or alter future APIs. Add new routers under `ProtocolandCodingService/app/` and include them in `app/main.py`.

