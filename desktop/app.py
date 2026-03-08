"""
Freelance Dev OS — Desktop Application
========================================

Launches the FastAPI web server in a background thread then opens it in a
native webview window using PyWebView. This produces a true cross-platform
desktop experience (macOS .app / Windows .exe) without any Electron overhead.

Usage:
    python desktop/app.py              # Run directly
    python run.py desktop              # Via unified launcher
    ./dist/FreelanceDevOS              # After packaging with PyInstaller
"""

from __future__ import annotations

import os
import sys
import time
import socket
import logging
import threading
import webbrowser
from pathlib import Path

# ── Ensure project root is on sys.path when run as a script ───────────────────
_PROJECT_ROOT = Path(__file__).parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

logger = logging.getLogger(__name__)

# ── Configuration ─────────────────────────────────────────────────────────────
APP_TITLE   = "Freelance Dev OS"
APP_WIDTH   = 1400
APP_HEIGHT  = 900
APP_MIN_W   = 900
APP_MIN_H   = 600
SERVER_PORT = int(os.getenv("DASHBOARD_PORT_DESKTOP", "8765"))
SERVER_HOST = "127.0.0.1"
SERVER_URL  = f"http://{SERVER_HOST}:{SERVER_PORT}"
STARTUP_TIMEOUT = 15   # seconds to wait for the server to be ready
DEBUG = os.getenv("FDO_DEBUG", "0") == "1"


# ── Server thread ─────────────────────────────────────────────────────────────

def _start_server() -> None:
    """Run the FastAPI/uvicorn server (blocking — run in daemon thread)."""
    try:
        import uvicorn
        from dashboard.main import app

        uvicorn.run(
            app,
            host=SERVER_HOST,
            port=SERVER_PORT,
            log_level="debug" if DEBUG else "error",
            access_log=DEBUG,
        )
    except Exception as e:
        logger.error(f"Server failed to start: {e}")


def _wait_for_server(timeout: int = STARTUP_TIMEOUT) -> bool:
    """Poll the server until it accepts connections or timeout expires."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((SERVER_HOST, SERVER_PORT), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.2)
    return False


# ── Desktop Window ────────────────────────────────────────────────────────────

def _get_icon_path() -> str | None:
    """Return path to the app icon if it exists."""
    candidates = [
        _PROJECT_ROOT / "desktop" / "icon.icns",   # macOS
        _PROJECT_ROOT / "desktop" / "icon.ico",    # Windows
        _PROJECT_ROOT / "desktop" / "icon.png",    # Linux
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return None


def _build_menu(window) -> list:
    """Build native menu items (PyWebView Menu API)."""
    try:
        import webview

        def _open_devtools():
            window.evaluate_js("window.open('about:blank','_blank')")

        def _reload():
            window.load_url(SERVER_URL)

        def _open_api_docs():
            webbrowser.open(f"{SERVER_URL}/api/docs")

        menu_items = [
            webview.menu.Menu("File", [
                webview.menu.MenuAction("Reload", _reload),
                webview.menu.MenuSeparator(),
                webview.menu.MenuAction("Quit", window.destroy),
            ]),
            webview.menu.Menu("View", [
                webview.menu.MenuAction("Dashboard Home", lambda: window.load_url(SERVER_URL + "/")),
                webview.menu.MenuAction("Projects",       lambda: window.load_url(SERVER_URL + "/projects")),
                webview.menu.MenuAction("Clients",        lambda: window.load_url(SERVER_URL + "/clients")),
                webview.menu.MenuAction("Revenue",        lambda: window.load_url(SERVER_URL + "/revenue")),
                webview.menu.MenuAction("Pipeline",       lambda: window.load_url(SERVER_URL + "/pipeline")),
                webview.menu.MenuAction("Time Tracking",  lambda: window.load_url(SERVER_URL + "/time-tracking")),
                webview.menu.MenuSeparator(),
                webview.menu.MenuAction("Settings",       lambda: window.load_url(SERVER_URL + "/settings")),
            ]),
            webview.menu.Menu("Help", [
                webview.menu.MenuAction("API Documentation", _open_api_docs),
                webview.menu.MenuAction("System Health",     lambda: window.load_url(SERVER_URL + "/health")),
            ]),
        ]
        return menu_items
    except (ImportError, AttributeError):
        return []


def run_desktop() -> None:
    """Main entry point: start server + open webview window."""
    logging.basicConfig(
        level=logging.DEBUG if DEBUG else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # ── 1. Start server in background ─────────────────────────────────────────
    logger.info(f"Starting embedded server on {SERVER_URL} …")
    server_thread = threading.Thread(target=_start_server, name="fdo-server", daemon=True)
    server_thread.start()

    # ── 2. Wait for server to be ready ────────────────────────────────────────
    print(f"\n  🚀 Freelance Dev OS — Starting up …")
    if not _wait_for_server():
        print("  ❌ Server failed to start within timeout. Aborting.")
        sys.exit(1)
    print(f"  ✓ Server ready at {SERVER_URL}\n")

    # ── 3. Try PyWebView, fall back to browser ────────────────────────────────
    try:
        import webview

        window = webview.create_window(
            title=APP_TITLE,
            url=SERVER_URL,
            width=APP_WIDTH,
            height=APP_HEIGHT,
            min_size=(APP_MIN_W, APP_MIN_H),
            resizable=True,
            shadow=True,
            confirm_close=False,
            background_color="#0d1117",
            text_select=True,
        )

        menu = _build_menu(window)

        logger.info("Launching PyWebView window …")
        webview.start(
            menu=menu if menu else None,
            debug=DEBUG,
            http_server=False,
            icon=_get_icon_path(),
        )

    except ImportError:
        # PyWebView not installed — open in default browser
        logger.warning("pywebview not installed — opening in default browser")
        print(f"  ℹ️  Opening {SERVER_URL} in your browser …")
        webbrowser.open(SERVER_URL)

        # Keep main thread alive so the server stays running
        print("  Press Ctrl+C to quit.\n")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n  Shutting down.")

    except Exception as e:
        logger.exception(f"Unexpected desktop error: {e}")
        sys.exit(1)


# ── Entry Point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_desktop()
