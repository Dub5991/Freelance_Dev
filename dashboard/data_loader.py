"""
Data Loader for Dashboard

Loads and aggregates data from existing MCP server JSON files.
"""

import json
import logging
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

from .config import DATA_DIR, PROJECT_ROOT

logger = logging.getLogger(__name__)


class DataLoader:
    """Load and aggregate data from MCP server data files."""
    
    def __init__(self, data_dir: Path = DATA_DIR):
        """Initialize data loader with data directory."""
        self.data_dir = data_dir
        self.project_root = PROJECT_ROOT
        
    def _load_json(self, filename: str, default: Any = None) -> Any:
        """Load JSON file from data directory."""
        filepath = self.data_dir / filename
        if not filepath.exists():
            logger.warning(f"File not found: {filepath}")
            return default if default is not None else {}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load {filename}: {e}")
            return default if default is not None else {}
    
    def _load_yaml(self, filepath: Path, default: Any = None) -> Any:
        """Load YAML file."""
        if not filepath.exists():
            logger.warning(f"File not found: {filepath}")
            return default if default is not None else {}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except (yaml.YAMLError, IOError) as e:
            logger.error(f"Failed to load {filepath}: {e}")
            return default if default is not None else {}
    
    def load_work_data(self) -> Dict[str, Any]:
        """Load task and hours data from work server."""
        vault_path = self.project_root / "vault"
        tasks_dir = vault_path / "03-Tasks"
        
        tasks_file = tasks_dir / "tasks.yaml"
        hours_file = tasks_dir / "hours.yaml"
        
        tasks = self._load_yaml(tasks_file, default=[])
        hours = self._load_yaml(hours_file, default=[])
        
        return {
            "tasks": tasks if isinstance(tasks, list) else [],
            "hours": hours if isinstance(hours, list) else []
        }
    
    def load_client_data(self) -> Dict[str, Any]:
        """Load client data from client server."""
        return self._load_json("client_data.json", default={
            "clients": {},
            "meetings": {},
            "health_scores": {}
        })
    
    def load_billing_data(self) -> Dict[str, Any]:
        """Load billing data from billing server."""
        return self._load_json("billing_data.json", default={
            "invoices": {},
            "payments": {},
            "revenue": {}
        })
    
    def load_llc_ops_data(self) -> Dict[str, Any]:
        """Load LLC operations data."""
        return self._load_json("llc_ops_data.json", default={
            "expenses": {},
            "tax_estimates": {},
            "compliance": {}
        })
    
    def load_onboarding_data(self) -> Dict[str, Any]:
        """Load onboarding data."""
        return self._load_json("onboarding_data.json", default={
            "workflows": {},
            "sows": {}
        })
    
    def load_career_data(self) -> Dict[str, Any]:
        """Load career development data."""
        return self._load_json("career_data.json", default={
            "skills": {},
            "portfolio": {},
            "rates": {}
        })
    
    def load_all_data(self) -> Dict[str, Any]:
        """Load all data from MCP servers."""
        return {
            "work": self.load_work_data(),
            "clients": self.load_client_data(),
            "billing": self.load_billing_data(),
            "llc_ops": self.load_llc_ops_data(),
            "onboarding": self.load_onboarding_data(),
            "career": self.load_career_data()
        }
    
    def get_overview_stats(self) -> Dict[str, Any]:
        """Get overview statistics for dashboard home."""
        data = self.load_all_data()
        
        # Work stats
        tasks = data["work"]["tasks"]
        active_tasks = [t for t in tasks if t.get("status") != "done"]
        
        # Client stats
        clients_data = data["clients"].get("clients", {})
        active_clients = [c for c in clients_data.values() if c.get("status") == "active"]
        
        # Billing stats
        invoices = data["billing"].get("invoices", {})
        paid_invoices = [i for i in invoices.values() if i.get("status") == "paid"]
        pending_invoices = [i for i in invoices.values() if i.get("status") in ["sent", "pending"]]
        overdue_invoices = [i for i in invoices.values() if i.get("status") == "overdue"]
        
        total_revenue = sum(float(i.get("total", 0)) for i in paid_invoices)
        pending_revenue = sum(float(i.get("total", 0)) for i in pending_invoices)
        
        # Hours stats
        hours_entries = data["work"]["hours"]
        current_month = datetime.now().strftime("%Y-%m")
        month_hours = [h for h in hours_entries if h.get("date", "").startswith(current_month)]
        total_hours_month = sum(float(h.get("hours", 0)) for h in month_hours)
        billable_hours_month = sum(float(h.get("hours", 0)) for h in month_hours if h.get("billable"))
        
        return {
            "active_projects": len(active_tasks),
            "active_clients": len(active_clients),
            "total_clients": len(clients_data),
            "total_revenue": total_revenue,
            "pending_revenue": pending_revenue,
            "paid_invoices": len(paid_invoices),
            "pending_invoices": len(pending_invoices),
            "overdue_invoices": len(overdue_invoices),
            "hours_this_month": total_hours_month,
            "billable_hours_month": billable_hours_month,
            "utilization_rate": (billable_hours_month / total_hours_month * 100) if total_hours_month > 0 else 0
        }
    
    def get_project_list(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of projects with details."""
        work_data = self.load_work_data()
        tasks = work_data["tasks"]
        hours_entries = work_data["hours"]
        
        projects = []
        for task in tasks:
            if status and task.get("status") != status:
                continue
            
            # Calculate hours logged for this task
            task_id = task.get("id")
            task_hours = [h for h in hours_entries if h.get("task_id") == task_id]
            hours_logged = sum(float(h.get("hours", 0)) for h in task_hours)
            
            projects.append({
                "id": task_id,
                "title": task.get("title", "Untitled"),
                "client": task.get("client", "N/A"),
                "status": task.get("status", "pending"),
                "priority": task.get("priority", "P3"),
                "billable": task.get("billable", False),
                "estimated_hours": task.get("estimated_hours", 0),
                "hours_logged": hours_logged,
                "created_at": task.get("created_at", ""),
                "due_date": task.get("due_date", "")
            })
        
        return projects
    
    def get_client_list(self) -> List[Dict[str, Any]]:
        """Get list of clients with health scores."""
        client_data = self.load_client_data()
        clients = client_data.get("clients", {})
        health_scores = client_data.get("health_scores", {})
        
        client_list = []
        for client_id, client_info in clients.items():
            health = health_scores.get(client_id, {})
            client_list.append({
                "id": client_id,
                "name": client_info.get("name", "Unknown"),
                "email": client_info.get("email", ""),
                "company": client_info.get("company", ""),
                "status": client_info.get("status", "active"),
                "health_score": health.get("score", 0),
                "health_status": health.get("status", "unknown"),
                "created_at": client_info.get("created_at", "")
            })
        
        return client_list
    
    def get_revenue_data(self, months: int = 12) -> Dict[str, Any]:
        """Get revenue data for the last N months."""
        billing_data = self.load_billing_data()
        invoices = billing_data.get("invoices", {})
        
        # Group revenue by month
        monthly_revenue = {}
        for invoice in invoices.values():
            if invoice.get("status") == "paid":
                invoice_date = invoice.get("issue_date", "")
                if invoice_date:
                    month_key = invoice_date[:7]  # YYYY-MM
                    amount = float(invoice.get("total", 0))
                    monthly_revenue[month_key] = monthly_revenue.get(month_key, 0) + amount
        
        # Get last N months
        today = date.today()
        result = {}
        for i in range(months - 1, -1, -1):
            month_date = date(today.year, today.month, 1) - timedelta(days=i * 30)
            month_key = month_date.strftime("%Y-%m")
            result[month_key] = monthly_revenue.get(month_key, 0)
        
        return {
            "monthly": result,
            "total": sum(result.values()),
            "average": sum(result.values()) / len(result) if result else 0
        }
    
    def get_pipeline_data(self) -> Dict[str, Any]:
        """Get sales pipeline data."""
        onboarding_data = self.load_onboarding_data()
        workflows = onboarding_data.get("workflows", {})
        
        pipeline_stages = {
            "leads": [],
            "proposals": [],
            "contracts": [],
            "active": []
        }
        
        for workflow_id, workflow in workflows.items():
            stage = workflow.get("stage", "leads")
            if stage in pipeline_stages:
                pipeline_stages[stage].append({
                    "id": workflow_id,
                    "client_name": workflow.get("client_name", "Unknown"),
                    "value": workflow.get("estimated_value", 0),
                    "stage": stage,
                    "created_at": workflow.get("created_at", "")
                })
        
        return {
            "stages": pipeline_stages,
            "conversion_rates": {
                "lead_to_proposal": self._calc_conversion(
                    len(pipeline_stages["proposals"]),
                    len(pipeline_stages["leads"])
                ),
                "proposal_to_contract": self._calc_conversion(
                    len(pipeline_stages["contracts"]),
                    len(pipeline_stages["proposals"])
                ),
                "contract_to_active": self._calc_conversion(
                    len(pipeline_stages["active"]),
                    len(pipeline_stages["contracts"])
                )
            }
        }
    
    def _calc_conversion(self, converted: int, total: int) -> float:
        """Calculate conversion rate percentage."""
        if total == 0:
            return 0.0
        return round((converted / total) * 100, 1)
    
    def get_time_tracking_data(self, days: int = 30) -> Dict[str, Any]:
        """Get time tracking data for the last N days."""
        work_data = self.load_work_data()
        hours_entries = work_data["hours"]
        
        # Filter to last N days
        cutoff_date = (date.today() - timedelta(days=days)).isoformat()
        recent_hours = [h for h in hours_entries if h.get("date", "") >= cutoff_date]
        
        # Aggregate by client
        by_client = {}
        by_date = {}
        
        for entry in recent_hours:
            client = entry.get("client", "Unassigned")
            hours = float(entry.get("hours", 0))
            billable = entry.get("billable", False)
            entry_date = entry.get("date", "")
            
            if client not in by_client:
                by_client[client] = {"billable": 0, "non_billable": 0}
            
            if billable:
                by_client[client]["billable"] += hours
            else:
                by_client[client]["non_billable"] += hours
            
            if entry_date:
                by_date[entry_date] = by_date.get(entry_date, 0) + hours
        
        total_hours = sum(h.get("hours", 0) for h in recent_hours)
        billable_hours = sum(h.get("hours", 0) for h in recent_hours if h.get("billable"))
        
        return {
            "total_hours": total_hours,
            "billable_hours": billable_hours,
            "non_billable_hours": total_hours - billable_hours,
            "utilization_rate": (billable_hours / total_hours * 100) if total_hours > 0 else 0,
            "by_client": by_client,
            "by_date": by_date
        }


if __name__ == "__main__":
    """Test data loader functionality."""
    logging.basicConfig(level=logging.INFO)
    
    loader = DataLoader()
    
    print("\n=== Overview Stats ===")
    overview = loader.get_overview_stats()
    for key, value in overview.items():
        print(f"{key}: {value}")
    
    print("\n=== Projects ===")
    projects = loader.get_project_list()
    print(f"Total projects: {len(projects)}")
    
    print("\n=== Clients ===")
    clients = loader.get_client_list()
    print(f"Total clients: {len(clients)}")
    
    print("\n=== Revenue Data ===")
    revenue = loader.get_revenue_data(months=6)
    print(f"Total revenue (6 months): ${revenue['total']:.2f}")
    print(f"Average monthly: ${revenue['average']:.2f}")
