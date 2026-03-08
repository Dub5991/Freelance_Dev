"""
Dashboard Configuration - Freelance Dev OS

All configuration for the web dashboard including auth, security, and UX settings.
"""

import os
import secrets
from pathlib import Path

from core.security import get_or_create_secret_key, hash_password

# ─── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
PROJECT_ROOT = BASE_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
SECRETS_DIR = PROJECT_ROOT / ".secrets"

# ─── Server Settings ───────────────────────────────────────────────────────────
DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "0.0.0.0")
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "8000"))
DASHBOARD_PORT_DESKTOP = int(os.getenv("DASHBOARD_PORT_DESKTOP", "8765"))
DASHBOARD_RELOAD = os.getenv("DASHBOARD_RELOAD", "True").lower() == "true"

# ─── Appearance ────────────────────────────────────────────────────────────────
DASHBOARD_TITLE = os.getenv("DASHBOARD_TITLE", "Freelance Dev OS")
DASHBOARD_THEME = os.getenv("DASHBOARD_THEME", "dark")  # "dark" | "light"

# ─── Auto-refresh ──────────────────────────────────────────────────────────────
AUTO_REFRESH_INTERVAL = int(os.getenv("AUTO_REFRESH_INTERVAL", "300"))  # seconds

# ─── Data Limits ───────────────────────────────────────────────────────────────
MAX_RECENT_ITEMS = int(os.getenv("MAX_RECENT_ITEMS", "10"))
MAX_CHART_DATAPOINTS = int(os.getenv("MAX_CHART_DATAPOINTS", "12"))

# ─── Feature Flags ─────────────────────────────────────────────────────────────
ENABLE_API = os.getenv("ENABLE_API", "True").lower() == "true"
ENABLE_CORS = os.getenv("ENABLE_CORS", "True").lower() == "true"
ENABLE_WEBSOCKET = os.getenv("ENABLE_WEBSOCKET", "True").lower() == "true"
AUTH_ENABLED = os.getenv("AUTH_ENABLED", "True").lower() == "true"

# ─── CORS ──────────────────────────────────────────────────────────────────────
_raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:8000,http://127.0.0.1:8765")
CORS_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()]
CORS_CREDENTIALS = os.getenv("CORS_CREDENTIALS", "True").lower() == "true"
CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_HEADERS = ["*"]

# ─── Authentication ────────────────────────────────────────────────────────────
# Secret key: loaded from .secrets/secret.key if present, else generated once.
_secret_key_file = SECRETS_DIR / "secret.key"
AUTH_SECRET_KEY: str = os.getenv(
    "AUTH_SECRET_KEY",
    get_or_create_secret_key(_secret_key_file),
)
AUTH_ALGORITHM = "HS256"
AUTH_TOKEN_EXPIRE_MINUTES = int(os.getenv("AUTH_TOKEN_EXPIRE_MINUTES", "60"))

# Dashboard credentials
# In production set DASHBOARD_PASSWORD_HASH (bcrypt) in .env.
# If only DASHBOARD_PASSWORD is set, it will be hashed at startup.
DASHBOARD_USERNAME: str = os.getenv("DASHBOARD_USERNAME", "admin")

_plain_pw: str = os.getenv("DASHBOARD_PASSWORD", "")
_hashed_pw: str = os.getenv("DASHBOARD_PASSWORD_HASH", "")

if _hashed_pw:
    DASHBOARD_PASSWORD_HASH: str = _hashed_pw
elif _plain_pw:
    DASHBOARD_PASSWORD_HASH = hash_password(_plain_pw)
else:
    # Auto-generate a password on first run and print it once
    _auto_pw = secrets.token_urlsafe(16)
    DASHBOARD_PASSWORD_HASH = hash_password(_auto_pw)
    print(
        f"\n[Freelance Dev OS] Auto-generated dashboard password: {_auto_pw}\n"
        "  Set DASHBOARD_PASSWORD or DASHBOARD_PASSWORD_HASH in .env to make it permanent.\n"
    )

# ─── Rate Limiting ─────────────────────────────────────────────────────────────
RATE_LIMIT_DEFAULT = os.getenv("RATE_LIMIT_DEFAULT", "120/minute")
RATE_LIMIT_AUTH = os.getenv("RATE_LIMIT_AUTH", "10/minute")   # Stricter for login endpoint
RATE_LIMIT_API = os.getenv("RATE_LIMIT_API", "200/minute")
