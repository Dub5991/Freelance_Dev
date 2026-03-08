"""
Authentication Module - Freelance Dev OS Dashboard

Provides JWT-based authentication routes, user verification,
and FastAPI security dependencies.
"""

import logging
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from core.security import (
    verify_password,
    hash_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from .config import (
    AUTH_SECRET_KEY,
    AUTH_ENABLED,
    DASHBOARD_USERNAME,
    DASHBOARD_PASSWORD_HASH,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

# ─── Pydantic Schemas ──────────────────────────────────────────────────────────

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60


class UserInfo(BaseModel):
    username: str
    role: str = "admin"


# ─── User Verification ─────────────────────────────────────────────────────────

def authenticate_user(username: str, password: str) -> Optional[UserInfo]:
    """Verify credentials against configured username/password."""
    if username != DASHBOARD_USERNAME:
        return None
    if not verify_password(password, DASHBOARD_PASSWORD_HASH):
        return None
    return UserInfo(username=username)


# ─── Token Extraction ──────────────────────────────────────────────────────────

def _extract_token(request: Request, bearer_token: Optional[str]) -> Optional[str]:
    """Try cookie first, then Authorization header."""
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        return cookie_token
    return bearer_token


# ─── Dependencies ──────────────────────────────────────────────────────────────

async def get_current_user(
    request: Request,
    bearer_token: Optional[str] = Depends(oauth2_scheme),
) -> Optional[UserInfo]:
    """
    FastAPI dependency that extracts and validates the current authenticated user.
    Returns None (rather than raising) so routes can handle unauthenticated state
    differently (redirect vs 401).
    """
    if not AUTH_ENABLED:
        return UserInfo(username="admin")

    token = _extract_token(request, bearer_token)
    if not token:
        return None

    payload = decode_token(token, AUTH_SECRET_KEY)
    if not payload:
        return None

    username: Optional[str] = payload.get("sub")
    if not username:
        return None

    return UserInfo(username=username)


async def require_auth(
    current_user: Optional[UserInfo] = Depends(get_current_user),
) -> UserInfo:
    """Dependency that raises 401 if not authenticated."""
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


# ─── Auth Routes ───────────────────────────────────────────────────────────────

@router.post("/login", response_model=TokenResponse)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Authenticate with username and password.
    Sets an HTTP-only access_token cookie and returns the token in the body.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username},
        secret_key=AUTH_SECRET_KEY,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username},
        secret_key=AUTH_SECRET_KEY,
    )

    # Set HTTP-only secure cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,   # Set True in production behind HTTPS
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=30 * 24 * 3600,
        path="/auth/refresh",
    )

    logger.info(f"User '{user.username}' logged in successfully")
    return TokenResponse(access_token=access_token)


@router.post("/logout")
async def logout(response: Response):
    """Clear authentication cookies."""
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/auth/refresh")
    return {"message": "Logged out successfully"}


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    response: Response,
    refresh_token: Optional[str] = Cookie(default=None),
):
    """Exchange a refresh token for a new access token."""
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token")

    payload = decode_token(refresh_token, AUTH_SECRET_KEY)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    username = payload.get("sub")
    new_access = create_access_token(
        data={"sub": username},
        secret_key=AUTH_SECRET_KEY,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    response.set_cookie(
        key="access_token",
        value=new_access,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    return TokenResponse(access_token=new_access)


@router.get("/me", response_model=UserInfo)
async def me(current_user: UserInfo = Depends(require_auth)):
    """Return information about the currently authenticated user."""
    return current_user
