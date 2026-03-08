#!/usr/bin/env python3
"""
Freelance Dev OS — Unified Launcher
=====================================

Run as web server or desktop application from a single entry point.

Usage:
    python run.py                 # Auto: desktop if pywebview available, else web
    python run.py web             # Force web server mode
    python run.py desktop         # Force desktop (PyWebView) mode
    python run.py web --port 9000 # Custom port
    python run.py web --host 0.0.0.0

Environment:
    AUTH_ENABLED=False            # Disable login (useful for development)
    DASHBOARD_PASSWORD=secret     # Set login password
    FDO_DEBUG=1                   # Enable debug logging
"""

from __future__ import annotations

import sys
import os
import argparse
import logging
from pathlib import Path

# ── Ensure project root is on path ────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ── Load .env early ───────────────────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass


def _run_web(host: str, port: int, reload: bool, debug: bool) -> None:
    """Start the FastAPI dashboard server with uvicorn."""
    try:
        import uvicorn
    except ImportError:
        print("  ❌  uvicorn not installed. Run: pip install uvicorn[standard]")
        sys.exit(1)

    from dashboard.config import DASHBOARD_TITLE
    print(f"\n  🚀  {DASHBOARD_TITLE}")
    print(f"  ══════════════════════════════════")
    print(f"  Mode:   Web Server")
    print(f"  URL:    http://{host}:{port}")
    print(f"  Auth:   {os.getenv('AUTH_ENABLED', 'True')}")
    print(f"  Reload: {reload}")
    print(f"  Press Ctrl+C to stop.\n")

    uvicorn.run(
        "dashboard.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="debug" if debug else "info",
        access_log=debug,
    )


def _run_desktop(debug: bool) -> None:
    """Launch the desktop PyWebView wrapper."""
    from desktop.app import run_desktop
    if debug:
        os.environ["FDO_DEBUG"] = "1"
    run_desktop()


def _has_pywebview() -> bool:
    """Return True if pywebview is importable."""
    try:
        import webview  # noqa: F401
        return True
    except ImportError:
        return False


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python run.py",
        description="Freelance Dev OS — Unified Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["web", "desktop"],
        default=None,
        help="Launch mode: 'web' (browser) or 'desktop' (native window). Default: auto-detect.",
    )
    parser.add_argument("--host",  default=os.getenv("DASHBOARD_HOST", "127.0.0.1"), help="Web server host")
    parser.add_argument("--port",  type=int, default=int(os.getenv("DASHBOARD_PORT", "8000")), help="Web server port")
    parser.add_argument("--reload", action="store_true", default=False, help="Enable hot-reload (dev)")
    parser.add_argument("--debug",  action="store_true", default=os.getenv("FDO_DEBUG") == "1", help="Debug logging")

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # Auto-detect mode
    mode = args.mode
    if mode is None:
        mode = "desktop" if _has_pywebview() else "web"

    if mode == "desktop":
        if not _has_pywebview():
            print("  ⚠️   pywebview not installed — falling back to web mode.")
            print("       Install with: pip install pywebview\n")
            mode = "web"

    if mode == "web":
        _run_web(host=args.host, port=args.port, reload=args.reload, debug=args.debug)
    else:
        _run_desktop(debug=args.debug)


if __name__ == "__main__":
    main()
