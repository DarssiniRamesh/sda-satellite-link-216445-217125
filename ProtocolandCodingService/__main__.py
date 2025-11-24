"""
Module entrypoint to run ProtocolandCodingService with `python -m ProtocolandCodingService`.

Resolves HOST/PORT from environment variables with defaults:
- PORT: defaults to 3002
- HOST: defaults to 0.0.0.0

This runner avoids shell-specific behavior and can be used in environments that prefer
python module execution.
"""

import os
import sys

# PUBLIC_INTERFACE
def resolve_host_port() -> tuple[str, int]:
    """Resolve HOST and PORT from environment with defaults.

    Returns:
        tuple[str, int]: Host and port values.
    """
    host = os.getenv("HOST", "0.0.0.0")
    port_str = os.getenv("PORT", "3002")
    try:
        port = int(port_str)
    except ValueError:
        # Fall back to default if invalid
        port = 3002
    return host, port


def main() -> int:
    """Start the uvicorn server for app.main:app using env HOST/PORT defaults."""
    try:
        import uvicorn
    except Exception as exc:  # pragma: no cover
        print(f"[ERROR] uvicorn not installed or failed to import: {exc}", file=sys.stderr)
        return 1

    host, port = resolve_host_port()
    print(f"[INFO] Launching uvicorn app.main:app on {host}:{port}")
    try:
        uvicorn.run("app.main:app", host=host, port=port)
    except KeyboardInterrupt:
        # Treat as clean shutdown
        print("[INFO] KeyboardInterrupt received, shutting down cleanly.")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
