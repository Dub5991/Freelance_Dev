"""
FastAPI Dashboard Application - Freelance Dev OS

Enhanced web dashboard with JWT auth, WebSocket real-time updates,
rate limiting, security headers, and a modern Alpine.js frontend.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Optional, Set

from fastapi import FastAPI, Request, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from .config import (
    DASHBOARD_TITLE,
    TEMPLATES_DIR,
    STATIC_DIR,
    ENABLE_CORS,
    CORS_ORIGINS,
    CORS_CREDENTIALS,
    CORS_METHODS,
    CORS_HEADERS,
    MAX_RECENT_ITEMS,
    AUTH_ENABLED,
    ENABLE_WEBSOCKET,
    RATE_LIMIT_DEFAULT,
    RATE_LIMIT_AUTH,
    RATE_LIMIT_API,
    DASHBOARD_THEME,
)
from .data_loader import DataLoader
from .auth import router as auth_router, get_current_user, require_auth, UserInfo
from .middleware import register_middleware, limiter

# ─── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ─── App Initialisation ────────────────────────────────────────────────────────
app = FastAPI(
    title=DASHBOARD_TITLE,
    description="Cross-platform business OS for freelance developers",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Register middleware (order: rate-limit → security-headers → logging)
register_middleware(app)

# CORS – restrict to configured origins in production
if ENABLE_CORS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=CORS_CREDENTIALS,
        allow_methods=CORS_METHODS,
        allow_headers=CORS_HEADERS,
    )

# Auth routes
app.include_router(auth_router)

# Static files & templates
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Data loader
data_loader = DataLoader()


# ─── WebSocket Connection Manager ──────────────────────────────────────────────

class ConnectionManager:
    """Manages active WebSocket connections for real-time broadcasting."""

    def __init__(self) -> None:
        self.active: Set[WebSocket] = set()

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self.active.add(ws)

    def disconnect(self, ws: WebSocket) -> None:
        self.active.discard(ws)

    async def broadcast(self, message: dict) -> None:
        dead: Set[WebSocket] = set()
        for ws in self.active:
            try:
                await ws.send_json(message)
            except Exception:
                dead.add(ws)
        self.active -= dead


ws_manager = ConnectionManager()


# ─── Template Context Helpers ──────────────────────────────────────────────────

def base_context(request: Request, user: Optional[UserInfo] = None) -> dict:
    """Base context injected into every template."""
    return {
        "request": request,
        "dashboard_title": DASHBOARD_TITLE,
        "current_year": datetime.now().year,
        "current_page": request.url.path,
        "theme": DASHBOARD_THEME,
        "auth_enabled": AUTH_ENABLED,
        "user": user,
        "ws_enabled": ENABLE_WEBSOCKET,
    }


def _redirect_to_login(request: Request) -> RedirectResponse:
    return RedirectResponse(url=f"/login?next={request.url.path}", status_code=302)


# ─── Auth Guard ────────────────────────────────────────────────────────────────

async def auth_or_redirect(
    request: Request,
    current_user: Optional[UserInfo] = Depends(get_current_user),
) -> Optional[UserInfo]:
    """For HTML routes: redirect unauthenticated users to /login."""
    if AUTH_ENABLED and current_user is None:
        return None   # caller handles redirect
    return current_user


# ─── Login / Logout HTML Routes ────────────────────────────────────────────────

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, next: Optional[str] = "/"):
    """Render the login page."""
    ctx = base_context(request)
    ctx["next_url"] = next
    return templates.TemplateResponse("login.html", ctx)


@app.get("/logout")
async def logout_page():
    """Clear cookies and redirect to login."""
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token", path="/")
    return response


# ─── HTML Dashboard Routes ─────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
@limiter.limit(RATE_LIMIT_DEFAULT)
async def index(
    request: Request,
    current_user: Optional[UserInfo] = Depends(auth_or_redirect),
):
    if AUTH_ENABLED and current_user is None:
        return _redirect_to_login(request)
    try:
        overview = data_loader.get_overview_stats()
        ctx = base_context(request, current_user)
        ctx.update({"overview": overview, "page_title": "Overview"})
        return templates.TemplateResponse("index.html", ctx)
    except Exception as e:
        logger.error(f"Error loading overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/projects", response_class=HTMLResponse)
@limiter.limit(RATE_LIMIT_DEFAULT)
async def projects(
    request: Request,
    status: Optional[str] = None,
    current_user: Optional[UserInfo] = Depends(auth_or_redirect),
):
    if AUTH_ENABLED and current_user is None:
        return _redirect_to_login(request)
    try:
        projects_list = data_loader.get_project_list(status=status)
        ctx = base_context(request, current_user)
        ctx.update({"projects": projects_list, "filter_status": status, "page_title": "Projects"})
        return templates.TemplateResponse("projects.html", ctx)
    except Exception as e:
        logger.error(f"Error loading projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/clients", response_class=HTMLResponse)
@limiter.limit(RATE_LIMIT_DEFAULT)
async def clients(
    request: Request,
    current_user: Optional[UserInfo] = Depends(auth_or_redirect),
):
    if AUTH_ENABLED and current_user is None:
        return _redirect_to_login(request)
    try:
        clients_list = data_loader.get_client_list()
        ctx = base_context(request, current_user)
        ctx.update({"clients": clients_list, "page_title": "Clients"})
        return templates.TemplateResponse("clients.html", ctx)
    except Exception as e:
        logger.error(f"Error loading clients: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/revenue", response_class=HTMLResponse)
@limiter.limit(RATE_LIMIT_DEFAULT)
async def revenue(
    request: Request,
    current_user: Optional[UserInfo] = Depends(auth_or_redirect),
):
    if AUTH_ENABLED and current_user is None:
        return _redirect_to_login(request)
    try:
        revenue_data = data_loader.get_revenue_data(months=12)
        billing_data = data_loader.load_billing_data()
        invoices = billing_data.get("invoices", {})
        invoice_list = [
            {
                "id": inv_id,
                "client": inv.get("client_name", "Unknown"),
                "amount": inv.get("total", 0),
                "status": inv.get("status", "pending"),
                "issue_date": inv.get("issue_date", ""),
                "due_date": inv.get("due_date", ""),
            }
            for inv_id, inv in list(invoices.items())[:MAX_RECENT_ITEMS]
        ]
        ctx = base_context(request, current_user)
        ctx.update({"revenue": revenue_data, "invoices": invoice_list, "page_title": "Revenue"})
        return templates.TemplateResponse("revenue.html", ctx)
    except Exception as e:
        logger.error(f"Error loading revenue: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pipeline", response_class=HTMLResponse)
@limiter.limit(RATE_LIMIT_DEFAULT)
async def pipeline(
    request: Request,
    current_user: Optional[UserInfo] = Depends(auth_or_redirect),
):
    if AUTH_ENABLED and current_user is None:
        return _redirect_to_login(request)
    try:
        pipeline_data = data_loader.get_pipeline_data()
        ctx = base_context(request, current_user)
        ctx.update({"pipeline": pipeline_data, "page_title": "Pipeline"})
        return templates.TemplateResponse("pipeline.html", ctx)
    except Exception as e:
        logger.error(f"Error loading pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/time-tracking", response_class=HTMLResponse)
@limiter.limit(RATE_LIMIT_DEFAULT)
async def time_tracking(
    request: Request,
    days: int = 30,
    current_user: Optional[UserInfo] = Depends(auth_or_redirect),
):
    if AUTH_ENABLED and current_user is None:
        return _redirect_to_login(request)
    try:
        time_data = data_loader.get_time_tracking_data(days=days)
        ctx = base_context(request, current_user)
        ctx.update({"time_data": time_data, "days": days, "page_title": "Time Tracking"})
        return templates.TemplateResponse("time_tracking.html", ctx)
    except Exception as e:
        logger.error(f"Error loading time tracking: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/settings", response_class=HTMLResponse)
@limiter.limit(RATE_LIMIT_DEFAULT)
async def settings(
    request: Request,
    current_user: UserInfo = Depends(require_auth),
):
    ctx = base_context(request, current_user)
    ctx["page_title"] = "Settings"
    return templates.TemplateResponse("settings.html", ctx)


# ─── JSON API Routes ───────────────────────────────────────────────────────────

@app.get("/api/overview")
@limiter.limit(RATE_LIMIT_API)
async def api_overview(
    request: Request,
    _: UserInfo = Depends(require_auth),
):
    try:
        return data_loader.get_overview_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects")
@limiter.limit(RATE_LIMIT_API)
async def api_projects(
    request: Request,
    status: Optional[str] = None,
    _: UserInfo = Depends(require_auth),
):
    try:
        return data_loader.get_project_list(status=status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/clients")
@limiter.limit(RATE_LIMIT_API)
async def api_clients(
    request: Request,
    _: UserInfo = Depends(require_auth),
):
    try:
        return data_loader.get_client_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/revenue")
@limiter.limit(RATE_LIMIT_API)
async def api_revenue(
    request: Request,
    months: int = 12,
    _: UserInfo = Depends(require_auth),
):
    try:
        return data_loader.get_revenue_data(months=months)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/pipeline")
@limiter.limit(RATE_LIMIT_API)
async def api_pipeline(
    request: Request,
    _: UserInfo = Depends(require_auth),
):
    try:
        return data_loader.get_pipeline_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/time-tracking")
@limiter.limit(RATE_LIMIT_API)
async def api_time_tracking(
    request: Request,
    days: int = 30,
    _: UserInfo = Depends(require_auth),
):
    try:
        return data_loader.get_time_tracking_data(days=days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/summary")
@limiter.limit(RATE_LIMIT_API)
async def api_summary(
    request: Request,
    _: UserInfo = Depends(require_auth),
):
    """Combined summary for dashboard widgets."""
    try:
        return {
            "overview": data_loader.get_overview_stats(),
            "revenue": data_loader.get_revenue_data(months=6),
            "pipeline": data_loader.get_pipeline_data(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── WebSocket Endpoint ────────────────────────────────────────────────────────

@app.websocket("/ws/live")
async def websocket_live(ws: WebSocket):
    """Real-time data push: sends overview stats every 30 seconds."""
    if not ENABLE_WEBSOCKET:
        await ws.close(code=1008)
        return

    await ws_manager.connect(ws)
    logger.info(f"WebSocket client connected: {ws.client}")
    try:
        # Send initial snapshot
        snapshot = data_loader.get_overview_stats()
        await ws.send_json({"type": "snapshot", "data": snapshot})

        # Keep alive + periodic refresh
        while True:
            try:
                # Wait for client ping or timeout
                data = await asyncio.wait_for(ws.receive_text(), timeout=30.0)
                if data == "ping":
                    await ws.send_json({"type": "pong"})
            except asyncio.TimeoutError:
                # Push refresh
                fresh = data_loader.get_overview_stats()
                await ws.send_json({"type": "refresh", "data": fresh})
    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected: {ws.client}")
    finally:
        ws_manager.disconnect(ws)


# ─── Health & Diagnostics ──────────────────────────────────────────────────────

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "auth_enabled": AUTH_ENABLED,
        "ws_enabled": ENABLE_WEBSOCKET,
    }


# ─── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    from .config import DASHBOARD_HOST, DASHBOARD_PORT, DASHBOARD_RELOAD

    logger.info(f"Starting Freelance Dev OS dashboard on {DASHBOARD_HOST}:{DASHBOARD_PORT}")
    uvicorn.run(
        "dashboard.main:app",
        host=DASHBOARD_HOST,
        port=DASHBOARD_PORT,
        reload=DASHBOARD_RELOAD,
        log_level="info",
    )
