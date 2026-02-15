"""
Freelance Dev - MCP Server Suite
AI-powered LLC operating system for freelance engineers.

Servers:
    - work_server: Task management with billable tracking
    - client_server: CRM with relationship health
    - billing_server: Stripe integration for invoicing
    - llc_ops_server: LLC operations dashboard
    - onboarding_server: Setup wizard
    - career_server: Career/skill tracking
"""

from .base_server import BaseMCPServer
from .work_server import get_server_info as work_info
from .client_server import ClientServer, get_server_info as client_info
from .billing_server import BillingServer, get_server_info as billing_info
from .llc_ops_server import LLCOpsServer, get_server_info as llc_ops_info
from .onboarding_server import OnboardingServer, get_server_info as onboarding_info
from .career_server import CareerServer, get_server_info as career_info

__version__ = "0.1.0"

__all__ = [
    "BaseMCPServer",
    "ClientServer",
    "BillingServer",
    "LLCOpsServer",
    "OnboardingServer",
    "CareerServer",
]

def get_all_servers() -> dict:
    """Get information about all available MCP servers."""
    return {
        "work": work_info(),
        "client": client_info(),
        "billing": billing_info(),
        "llc_ops": llc_ops_info(),
        "onboarding": onboarding_info(),
        "career": career_info()
    }