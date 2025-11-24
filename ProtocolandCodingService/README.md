# Protocol and Coding Service

FastAPI backend that handles synchronization, channel coding (5G NR LDPC FEC), frame construction (preamble, header, payload), scrambling, error control (CRC-16, CRC-32), and ARQ management.

This scaffolding provides:
- FastAPI app exposed at `app.main:app`
- Health endpoint at `/health`
- `requirements.txt` for dependencies
- `run.sh` script to install dependencies and start the service

## Port and environment configuration

- Default port: 3002
- You can override with environment variable: `PORT`
- Default host: `0.0.0.0` (override with `HOST`)

Examples:
```bash
# Default (PORT=3002)
cd sda-satellite-link-216445-217125/ProtocolandCodingService
./run.sh

# Override port
PORT=3100 ./run.sh

# Using .env (optional)
cp .env.example .env
# edit .env and set PORT=3002 or your desired value
./run.sh
```

Then visit:
- Health: http://localhost:3002/health
- OpenAPI docs: http://localhost:3002/docs
