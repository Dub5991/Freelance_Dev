"""
Core MCP (Model Context Protocol) Servers for Freelance LLC OS

This package contains all the MCP server implementations for managing
a freelance LLC operation including:
- Work/Task Management
- Client Relationship Management (CRM)
- Billing and Invoicing
- LLC Operations and Finances
- Career Development Tracking
- Onboarding and Setup
"""

__version__ = "1.0.0"
__author__ = "Freelance Dev Community"

# Import all server classes for easy access
from .work_server import WorkServer
from .client_server import ClientServer
from .billing_server import BillingServer
from .llc_ops_server import LLCOpsServer
from .onboarding_server import OnboardingServer
from .career_server import CareerServer

__all__ = [
    "WorkServer",
    "ClientServer",
    "BillingServer",
    "LLCOpsServer",
    "OnboardingServer",
    "CareerServer",
]
