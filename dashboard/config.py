"""
Dashboard Configuration

Configuration settings for the web dashboard.
"""

import os
from pathlib import Path
from typing import Optional

# Dashboard settings
DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "0.0.0.0")
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "8000"))
DASHBOARD_RELOAD = os.getenv("DASHBOARD_RELOAD", "True").lower() == "true"

# Paths
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
PROJECT_ROOT = BASE_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"

# Dashboard appearance
DASHBOARD_TITLE = os.getenv("DASHBOARD_TITLE", "Freelance Dev OS - CV/AI Engineering")
DASHBOARD_THEME = os.getenv("DASHBOARD_THEME", "dark")

# Refresh intervals (in seconds)
AUTO_REFRESH_INTERVAL = int(os.getenv("AUTO_REFRESH_INTERVAL", "300"))  # 5 minutes

# Data display limits
MAX_RECENT_ITEMS = int(os.getenv("MAX_RECENT_ITEMS", "10"))
MAX_CHART_DATAPOINTS = int(os.getenv("MAX_CHART_DATAPOINTS", "12"))

# Feature flags
ENABLE_API = os.getenv("ENABLE_API", "True").lower() == "true"
ENABLE_CORS = os.getenv("ENABLE_CORS", "True").lower() == "true"

# CORS settings
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_CREDENTIALS = os.getenv("CORS_CREDENTIALS", "True").lower() == "true"
CORS_METHODS = ["GET", "POST", "PUT", "DELETE"]
CORS_HEADERS = ["*"]
