"""
Freelance LLC Operating System - Core Package

Provides core functionality including:
- Configuration management
- Utility functions
- MCP server infrastructure
"""

from .config import Config
from .utils import (
    setup_logging,
    load_json,
    save_json,
    format_date,
    format_datetime,
    format_currency,
    generate_id,
    get_quarter,
    validate_email,
    validate_phone,
)

__version__ = "0.1.0"

__all__ = [
    "Config",
    "setup_logging",
    "load_json",
    "save_json",
    "format_date",
    "format_datetime",
    "format_currency",
    "generate_id",
    "get_quarter",
    "validate_email",
    "validate_phone",
]
