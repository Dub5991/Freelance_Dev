"""
Shared Utility Functions for Freelance LLC OS

Common helpers for date formatting, file I/O, validation, and data manipulation.
"""

import json
import logging
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Any, Optional, Union
from decimal import Decimal, ROUND_HALF_UP


def setup_logging(name: str, log_file: Optional[Path] = None, level: str = "INFO") -> logging.Logger:
    """
    Set up logging for a module.
    
    Args:
        name: Logger name (usually __name__)
        log_file: Optional log file path
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level.upper()))
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def load_json(filepath: Union[str, Path], default: Any = None) -> Any:
    """
    Load JSON file with error handling.
    
    Args:
        filepath: Path to JSON file
        default: Default value if file doesn't exist or is invalid
    
    Returns:
        Parsed JSON data or default value
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        return default if default is not None else {}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logging.warning(f"Failed to load JSON from {filepath}: {e}")
        return default if default is not None else {}


def save_json(filepath: Union[str, Path], data: Any, indent: int = 2) -> bool:
    """
    Save data to JSON file with error handling.
    
    Args:
        filepath: Path to JSON file
        data: Data to serialize
        indent: JSON indentation (default: 2)
    
    Returns:
        True if successful, False otherwise
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, default=str)
        return True
    except (IOError, TypeError) as e:
        logging.error(f"Failed to save JSON to {filepath}: {e}")
        return False


def format_date(dt: Optional[Union[datetime, date, str]] = None, fmt: str = "%Y-%m-%d") -> str:
    """
    Format date/datetime to string.
    
    Args:
        dt: Date/datetime object or ISO string (defaults to today)
        fmt: strftime format string
    
    Returns:
        Formatted date string
    """
    if dt is None:
        dt = date.today()
    elif isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt).date()
        except ValueError:
            return dt
    elif isinstance(dt, datetime):
        dt = dt.date()
    
    return dt.strftime(fmt)


def format_datetime(dt: Optional[Union[datetime, str]] = None, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime to string.
    
    Args:
        dt: Datetime object or ISO string (defaults to now)
        fmt: strftime format string
    
    Returns:
        Formatted datetime string
    """
    if dt is None:
        dt = datetime.now()
    elif isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except ValueError:
            return dt
    
    return dt.strftime(fmt)


def parse_date(date_str: str) -> Optional[date]:
    """
    Parse date string in various formats.
    
    Args:
        date_str: Date string to parse
    
    Returns:
        date object or None if parsing fails
    """
    formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%b %d, %Y",
        "%B %d, %Y",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    return None


def format_currency(amount: Union[float, Decimal, int], currency: str = "USD") -> str:
    """
    Format amount as currency.
    
    Args:
        amount: Numeric amount
        currency: Currency code (default: USD)
    
    Returns:
        Formatted currency string
    """
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
    }
    
    symbol = symbols.get(currency, currency + " ")
    
    if isinstance(amount, Decimal):
        amount = float(amount)
    
    return f"{symbol}{amount:,.2f}"


def calculate_percentage(part: float, total: float, decimal_places: int = 1) -> float:
    """
    Calculate percentage safely.
    
    Args:
        part: Part value
        total: Total value
        decimal_places: Decimal places to round to
    
    Returns:
        Percentage (0-100)
    """
    if total == 0:
        return 0.0
    
    percentage = (part / total) * 100
    return round(percentage, decimal_places)


def round_currency(amount: Union[float, Decimal], places: int = 2) -> Decimal:
    """
    Round currency amount properly.
    
    Args:
        amount: Amount to round
        places: Decimal places (default: 2)
    
    Returns:
        Rounded Decimal
    """
    if not isinstance(amount, Decimal):
        amount = Decimal(str(amount))
    
    quantize_str = '0.' + '0' * places
    return amount.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)


def generate_id(prefix: str, date_part: bool = True) -> str:
    """
    Generate a unique ID with optional date component.
    
    Args:
        prefix: ID prefix (e.g., 'inv', 'client', 'task')
        date_part: Include date in ID
    
    Returns:
        Generated ID string
    """
    if date_part:
        date_str = datetime.now().strftime("%Y%m%d")
        timestamp = datetime.now().strftime("%H%M%S")
        return f"{prefix}-{date_str}-{timestamp}"
    else:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{prefix}-{timestamp}"


def get_quarter(dt: Optional[Union[datetime, date]] = None) -> tuple[int, int]:
    """
    Get quarter and year for a date.
    
    Args:
        dt: Date/datetime (defaults to today)
    
    Returns:
        Tuple of (quarter, year)
    """
    if dt is None:
        dt = date.today()
    elif isinstance(dt, datetime):
        dt = dt.date()
    
    quarter = (dt.month - 1) // 3 + 1
    return quarter, dt.year


def get_quarter_dates(quarter: int, year: int) -> tuple[date, date]:
    """
    Get start and end dates for a quarter.
    
    Args:
        quarter: Quarter number (1-4)
        year: Year
    
    Returns:
        Tuple of (start_date, end_date)
    """
    if not 1 <= quarter <= 4:
        raise ValueError("Quarter must be between 1 and 4")
    
    start_month = (quarter - 1) * 3 + 1
    start_date = date(year, start_month, 1)
    
    if quarter == 4:
        end_date = date(year, 12, 31)
    else:
        end_month = quarter * 3
        # Get last day of the month
        if end_month == 12:
            end_date = date(year, 12, 31)
        else:
            end_date = date(year, end_month + 1, 1) - timedelta(days=1)
    
    return start_date, end_date


def validate_email(email: str) -> bool:
    """
    Basic email validation.
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid format, False otherwise
    """
    if not email or '@' not in email:
        return False
    
    parts = email.split('@')
    if len(parts) != 2:
        return False
    
    local, domain = parts
    if not local or not domain:
        return False
    
    if '.' not in domain:
        return False
    
    return True


def validate_phone(phone: str) -> bool:
    """
    Basic phone number validation.
    
    Args:
        phone: Phone number to validate
    
    Returns:
        True if valid format, False otherwise
    """
    # Remove common formatting characters
    cleaned = ''.join(c for c in phone if c.isdigit())
    
    # Check if we have 10-15 digits (covers most formats)
    return 10 <= len(cleaned) <= 15


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file system usage.
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    
    # Ensure we have something left
    if not filename:
        filename = "unnamed"
    
    return filename


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate string to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated
    
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def merge_dicts(base: dict, updates: dict, overwrite: bool = True) -> dict:
    """
    Merge two dictionaries.
    
    Args:
        base: Base dictionary
        updates: Updates to apply
        overwrite: Whether to overwrite existing keys
    
    Returns:
        Merged dictionary
    """
    result = base.copy()
    
    for key, value in updates.items():
        if overwrite or key not in result:
            result[key] = value
    
    return result
