"""
FastAPI Dashboard Application

Web dashboard for managing CV/AI freelance business with Freelance Dev OS.
"""

import logging
from datetime import datetime
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
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
    MAX_RECENT_ITEMS
)
from .data_loader import DataLoader

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=DASHBOARD_TITLE,
    description="Web dashboard for managing CV/AI freelance business",
    version="1.0.0"
)

# Add CORS middleware if enabled
if ENABLE_CORS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=CORS_CREDENTIALS,
        allow_methods=CORS_METHODS,
        allow_headers=CORS_HEADERS,
    )

# Setup static files and templates
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Initialize data loader
data_loader = DataLoader()

# Template context processor
def get_base_context(request: Request) -> dict:
    """Get base context for all templates."""
    return {
        "request": request,
        "dashboard_title": DASHBOARD_TITLE,
        "current_year": datetime.now().year,
        "current_page": request.url.path
    }


# HTML Routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Dashboard home page with overview."""
    try:
        overview = data_loader.get_overview_stats()
        context = get_base_context(request)
        context.update({
            "overview": overview,
            "page_title": "Overview"
        })
        return templates.TemplateResponse("index.html", context)
    except Exception as e:
        logger.error(f"Error loading overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/projects", response_class=HTMLResponse)
async def projects(request: Request, status: Optional[str] = None):
    """Projects view with active CV/AI projects."""
    try:
        projects_list = data_loader.get_project_list(status=status)
        context = get_base_context(request)
        context.update({
            "projects": projects_list,
            "filter_status": status,
            "page_title": "Projects"
        })
        return templates.TemplateResponse("projects.html", context)
    except Exception as e:
        logger.error(f"Error loading projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/clients", response_class=HTMLResponse)
async def clients(request: Request):
    """Clients view with health scores."""
    try:
        clients_list = data_loader.get_client_list()
        context = get_base_context(request)
        context.update({
            "clients": clients_list,
            "page_title": "Clients"
        })
        return templates.TemplateResponse("clients.html", context)
    except Exception as e:
        logger.error(f"Error loading clients: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/revenue", response_class=HTMLResponse)
async def revenue(request: Request):
    """Revenue and financial view."""
    try:
        revenue_data = data_loader.get_revenue_data(months=12)
        billing_data = data_loader.load_billing_data()
        invoices = billing_data.get("invoices", {})
        
        # Get invoice summaries
        invoice_list = []
        for inv_id, inv in list(invoices.items())[:MAX_RECENT_ITEMS]:
            invoice_list.append({
                "id": inv_id,
                "client": inv.get("client_name", "Unknown"),
                "amount": inv.get("total", 0),
                "status": inv.get("status", "pending"),
                "issue_date": inv.get("issue_date", ""),
                "due_date": inv.get("due_date", "")
            })
        
        context = get_base_context(request)
        context.update({
            "revenue": revenue_data,
            "invoices": invoice_list,
            "page_title": "Revenue"
        })
        return templates.TemplateResponse("revenue.html", context)
    except Exception as e:
        logger.error(f"Error loading revenue: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pipeline", response_class=HTMLResponse)
async def pipeline(request: Request):
    """Sales pipeline view."""
    try:
        pipeline_data = data_loader.get_pipeline_data()
        context = get_base_context(request)
        context.update({
            "pipeline": pipeline_data,
            "page_title": "Pipeline"
        })
        return templates.TemplateResponse("pipeline.html", context)
    except Exception as e:
        logger.error(f"Error loading pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/time-tracking", response_class=HTMLResponse)
async def time_tracking(request: Request, days: int = 30):
    """Time tracking view."""
    try:
        time_data = data_loader.get_time_tracking_data(days=days)
        context = get_base_context(request)
        context.update({
            "time_data": time_data,
            "days": days,
            "page_title": "Time Tracking"
        })
        return templates.TemplateResponse("time_tracking.html", context)
    except Exception as e:
        logger.error(f"Error loading time tracking: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# API Routes
@app.get("/api/overview")
async def api_overview():
    """API endpoint for overview stats."""
    try:
        return data_loader.get_overview_stats()
    except Exception as e:
        logger.error(f"API error in overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects")
async def api_projects(status: Optional[str] = None):
    """API endpoint for projects list."""
    try:
        return data_loader.get_project_list(status=status)
    except Exception as e:
        logger.error(f"API error in projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/clients")
async def api_clients():
    """API endpoint for clients list."""
    try:
        return data_loader.get_client_list()
    except Exception as e:
        logger.error(f"API error in clients: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/revenue")
async def api_revenue(months: int = 12):
    """API endpoint for revenue data."""
    try:
        return data_loader.get_revenue_data(months=months)
    except Exception as e:
        logger.error(f"API error in revenue: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/pipeline")
async def api_pipeline():
    """API endpoint for pipeline data."""
    try:
        return data_loader.get_pipeline_data()
    except Exception as e:
        logger.error(f"API error in pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/time-tracking")
async def api_time_tracking(days: int = 30):
    """API endpoint for time tracking data."""
    try:
        return data_loader.get_time_tracking_data(days=days)
    except Exception as e:
        logger.error(f"API error in time tracking: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    from .config import DASHBOARD_HOST, DASHBOARD_PORT, DASHBOARD_RELOAD
    
    logger.info(f"Starting dashboard on {DASHBOARD_HOST}:{DASHBOARD_PORT}")
    uvicorn.run(
        "dashboard.main:app",
        host=DASHBOARD_HOST,
        port=DASHBOARD_PORT,
        reload=DASHBOARD_RELOAD,
        log_level="info"
    )
