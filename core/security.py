"""
Security Module - Freelance Dev OS

Provides JWT authentication, password hashing, input sanitization,
and security utilities for the web dashboard.
"""

import re
import secrets
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Optional, Any, Dict
from pathlib import Path

from jose import JWTError, jwt
from passlib.context import CryptContext

logger = logging.getLogger(__name__)

# ─── Crypto Context ────────────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ─── JWT Configuration ─────────────────────────────────────────────────────────
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 30


# ─── Password Utilities ────────────────────────────────────────────────────────
def hash_password(plain_password: str) -> str:
    """Hash a plain text password using bcrypt."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


def generate_secure_password(length: int = 20) -> str:
    """Generate a cryptographically secure random password."""
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    return "".join(secrets.choice(alphabet) for _ in range(length))


# ─── JWT Token Utilities ───────────────────────────────────────────────────────
def create_access_token(
    data: Dict[str, Any],
    secret_key: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access",
    })
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)


def create_refresh_token(data: Dict[str, Any], secret_key: str) -> str:
    """Create a signed JWT refresh token (long-lived)."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh",
    })
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)


def decode_token(token: str, secret_key: str) -> Optional[Dict[str, Any]]:
    """Decode and verify a JWT token. Returns None if invalid."""
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        logger.warning(f"JWT decode error: {e}")
        return None


def is_token_expired(payload: Dict[str, Any]) -> bool:
    """Check if a decoded token payload is expired."""
    exp = payload.get("exp")
    if exp is None:
        return True
    return datetime.utcnow() > datetime.utcfromtimestamp(exp)


# ─── Secret Key Management ─────────────────────────────────────────────────────
def generate_secret_key() -> str:
    """Generate a cryptographically secure secret key (64 hex chars)."""
    return secrets.token_hex(32)


def get_or_create_secret_key(key_file: Optional[Path] = None) -> str:
    """
    Load secret key from file or environment; create and persist if absent.
    Falls back to generating an ephemeral key (not persisted).
    """
    if key_file and key_file.exists():
        key = key_file.read_text().strip()
        if len(key) >= 32:
            return key

    key = generate_secret_key()

    if key_file:
        try:
            key_file.parent.mkdir(parents=True, exist_ok=True)
            key_file.write_text(key)
            key_file.chmod(0o600)
            logger.info(f"Generated and saved new secret key to {key_file}")
        except OSError as e:
            logger.warning(f"Could not save secret key to {key_file}: {e}")

    return key


# ─── Input Sanitization ────────────────────────────────────────────────────────
_DISALLOWED_HTML = re.compile(r"<[^>]+>", re.IGNORECASE)
_PATH_TRAVERSAL = re.compile(r"\.\.[/\\]")
_NULL_BYTES = re.compile(r"\x00")
_SQL_KEYWORDS = re.compile(
    r"\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION|SCRIPT)\b",
    re.IGNORECASE,
)


def sanitize_string(value: str, max_length: int = 500) -> str:
    """
    Sanitize a user-supplied string:
    - Strip leading/trailing whitespace
    - Remove null bytes
    - Strip HTML tags
    - Prevent path traversal sequences
    - Truncate to max_length
    """
    if not isinstance(value, str):
        value = str(value)
    value = _NULL_BYTES.sub("", value)
    value = _DISALLOWED_HTML.sub("", value)
    value = _PATH_TRAVERSAL.sub("", value)
    return value.strip()[:max_length]


def is_safe_string(value: str) -> bool:
    """Return True when the string contains no obviously dangerous patterns."""
    if _NULL_BYTES.search(value):
        return False
    if _PATH_TRAVERSAL.search(value):
        return False
    return True


def sanitize_filename(name: str) -> str:
    """Produce a filesystem-safe filename."""
    name = _NULL_BYTES.sub("", name)
    name = re.sub(r'[^\w\s\-.]', "", name)
    name = re.sub(r'\s+', "_", name)
    return name[:100].strip("._")


def validate_email(email: str) -> bool:
    """Basic RFC-5322 email validation."""
    pattern = r'^[a-zA-Z0-9_.+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9.\-]+$'
    return bool(re.match(pattern, email.strip())) and len(email) <= 254


# ─── CSRF Token Utilities ──────────────────────────────────────────────────────
def generate_csrf_token() -> str:
    """Generate a URL-safe CSRF token."""
    return secrets.token_urlsafe(32)


def verify_csrf_token(token: str, expected: str) -> bool:
    """Constant-time comparison to prevent timing attacks."""
    return secrets.compare_digest(token, expected)


# ─── Audit Hashing ─────────────────────────────────────────────────────────────
def hash_for_audit(value: str) -> str:
    """SHA-256 hash of a value for audit log storage (non-reversible)."""
    return hashlib.sha256(value.encode()).hexdigest()


# ─── Security Headers ──────────────────────────────────────────────────────────
SECURITY_HEADERS: Dict[str, str] = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self' ws: wss:; "
        "frame-ancestors 'none';"
    ),
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
}
