"""
Client Server - MCP Server for CRM (Client Relationship Management)

Full async implementation for managing clients with:
- Client/prospect pages with YAML storage
- Relationship health tracking (score 1-10)
- Contract dates with renewal alerts (30 days before expiry)
- Meeting history, commitment tracking
- Internal vs External routing by email domain
"""

import asyncio
import os
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

VAULT_PATH = os.getenv("VAULT_PATH", "./vault")
PEOPLE_PATH = Path(VAULT_PATH) / "05-Areas" / "People"
COMPANIES_PATH = Path(VAULT_PATH) / "05-Areas" / "Companies"
RENEWAL_ALERT_DAYS = int(os.getenv("RENEWAL_ALERT_DAYS", 30))


class ClientServer:
    """Async MCP Server for client relationship management"""
    
    def __init__(self):
        self.server = Server("client-server")
        self.clients_cache = {}
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup all tool handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="create_client",
                    description="Create a new client or prospect",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Client/company name"},
                            "contact_name": {"type": "string", "description": "Primary contact name"},
                            "email": {"type": "string", "description": "Contact email"},
                            "phone": {"type": "string", "description": "Phone number"},
                            "type": {
                                "type": "string",
                                "enum": ["client", "prospect"],
                                "description": "Client or prospect"
                            },
                            "contract_start": {"type": "string", "description": "Contract start date YYYY-MM-DD"},
                            "contract_end": {"type": "string", "description": "Contract end date YYYY-MM-DD"},
                            "hourly_rate": {"type": "number", "description": "Hourly rate for this client"}
                        },
                        "required": ["name", "email", "type"]
                    }
                ),
                Tool(
                    name="get_client",
                    description="Get detailed information about a client",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Client name"}
                        },
                        "required": ["name"]
                    }
                ),
                Tool(
                    name="list_clients",
                    description="List all clients with optional filters",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["client", "prospect", "all"],
                                "description": "Filter by type"
                            },
                            "health_threshold": {
                                "type": "number",
                                "description": "Show clients with health score below threshold"
                            }
                        }
                    }
                ),
                Tool(
                    name="log_meeting",
                    description="Log a meeting with a client",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "client_name": {"type": "string", "description": "Client name"},
                            "date": {"type": "string", "description": "Meeting date YYYY-MM-DD"},
                            "notes": {"type": "string", "description": "Meeting notes"},
                            "attendees": {"type": "string", "description": "Comma-separated attendees"}
                        },
                        "required": ["client_name", "notes"]
                    }
                ),
                Tool(
                    name="add_commitment",
                    description="Add a commitment or action item for a client",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "client_name": {"type": "string", "description": "Client name"},
                            "commitment": {"type": "string", "description": "Commitment description"},
                            "due_date": {"type": "string", "description": "Due date YYYY-MM-DD"},
                            "owner": {
                                "type": "string",
                                "enum": ["me", "client"],
                                "description": "Who owns this commitment"
                            }
                        },
                        "required": ["client_name", "commitment", "owner"]
                    }
                ),
                Tool(
                    name="check_renewals",
                    description="Check for upcoming contract renewals",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "days_ahead": {
                                "type": "number",
                                "description": "Look ahead N days (default 30)"
                            }
                        }
                    }
                ),
                Tool(
                    name="get_client_health",
                    description="Get relationship health scores for all clients",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "min_score": {
                                "type": "number",
                                "description": "Filter clients with score below this"
                            }
                        }
                    }
                ),
                Tool(
                    name="update_health_score",
                    description="Update relationship health score for a client",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "client_name": {"type": "string", "description": "Client name"},
                            "score": {
                                "type": "number",
                                "minimum": 1,
                                "maximum": 10,
                                "description": "Health score 1-10"
                            },
                            "notes": {"type": "string", "description": "Notes on score change"}
                        },
                        "required": ["client_name", "score"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Route tool calls to appropriate handlers"""
            
            if name == "create_client":
                result = await self._create_client(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "get_client":
                result = await self._get_client(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "list_clients":
                result = await self._list_clients(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "log_meeting":
                result = await self._log_meeting(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "add_commitment":
                result = await self._add_commitment(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "check_renewals":
                result = await self._check_renewals(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "get_client_health":
                result = await self._get_client_health(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "update_health_score":
                result = await self._update_health_score(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def _create_client(
        self,
        name: str,
        email: str,
        type: str,
        contact_name: str = "",
        phone: str = "",
        contract_start: str = None,
        contract_end: str = None,
        hourly_rate: float = None
    ) -> Dict[str, Any]:
        """Create a new client or prospect"""
        
        # Determine if internal or external based on email domain
        domain = email.split('@')[1] if '@' in email else ""
        owner_domain = os.getenv("OWNER_EMAIL", "").split('@')[1] if '@' in os.getenv("OWNER_EMAIL", "") else ""
        is_internal = domain == owner_domain
        
        # Create client ID
        client_id = name.lower().replace(" ", "-")
        
        client = {
            "client_id": client_id,
            "name": name,
            "contact_name": contact_name,
            "email": email,
            "phone": phone,
            "type": type,
            "is_internal": is_internal,
            "health_score": 7,  # Default healthy score
            "hourly_rate": hourly_rate or float(os.getenv("DEFAULT_HOURLY_RATE", 150)),
            "contract_start": contract_start,
            "contract_end": contract_end,
            "meetings": [],
            "commitments": [],
            "health_history": [{
                "date": datetime.now().isoformat(),
                "score": 7,
                "notes": "Initial client setup"
            }],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        await self._save_client(client)
        
        return {
            "success": True,
            "client_id": client_id,
            "message": f"Client '{name}' created successfully",
            "is_internal": is_internal
        }
    
    async def _get_client(self, name: str) -> Dict[str, Any]:
        """Get detailed client information"""
        
        client = await self._load_client_by_name(name)
        if not client:
            return {"success": False, "error": f"Client '{name}' not found"}
        
        # Calculate days until contract renewal
        renewal_warning = None
        if client.get("contract_end"):
            end_date = datetime.fromisoformat(client["contract_end"]).date()
            days_until = (end_date - date.today()).days
            if 0 <= days_until <= RENEWAL_ALERT_DAYS:
                renewal_warning = f"Contract expires in {days_until} days!"
        
        return {
            "success": True,
            "client": client,
            "renewal_warning": renewal_warning
        }
    
    async def _list_clients(
        self,
        type: str = "all",
        health_threshold: float = None
    ) -> Dict[str, Any]:
        """List clients with filters"""
        
        clients = await self._load_all_clients()
        filtered_clients = []
        
        for client in clients:
            # Apply filters
            if type != "all" and client.get("type") != type:
                continue
            if health_threshold and client.get("health_score", 10) >= health_threshold:
                continue
            
            filtered_clients.append({
                "name": client["name"],
                "type": client["type"],
                "health_score": client.get("health_score", 0),
                "email": client["email"],
                "contract_end": client.get("contract_end")
            })
        
        return {
            "success": True,
            "count": len(filtered_clients),
            "clients": filtered_clients
        }
    
    async def _log_meeting(
        self,
        client_name: str,
        notes: str,
        date: str = None,
        attendees: str = ""
    ) -> Dict[str, Any]:
        """Log a meeting with a client"""
        
        client = await self._load_client_by_name(client_name)
        if not client:
            return {"success": False, "error": f"Client '{client_name}' not found"}
        
        meeting = {
            "date": date or datetime.now().isoformat(),
            "notes": notes,
            "attendees": attendees.split(",") if attendees else [],
            "logged_at": datetime.now().isoformat()
        }
        
        if "meetings" not in client:
            client["meetings"] = []
        client["meetings"].append(meeting)
        client["updated_at"] = datetime.now().isoformat()
        
        await self._save_client(client)
        
        return {
            "success": True,
            "message": f"Meeting logged for {client_name}"
        }
    
    async def _add_commitment(
        self,
        client_name: str,
        commitment: str,
        owner: str,
        due_date: str = None
    ) -> Dict[str, Any]:
        """Add a commitment or action item"""
        
        client = await self._load_client_by_name(client_name)
        if not client:
            return {"success": False, "error": f"Client '{client_name}' not found"}
        
        commitment_item = {
            "description": commitment,
            "owner": owner,
            "due_date": due_date,
            "status": "open",
            "created_at": datetime.now().isoformat()
        }
        
        if "commitments" not in client:
            client["commitments"] = []
        client["commitments"].append(commitment_item)
        client["updated_at"] = datetime.now().isoformat()
        
        await self._save_client(client)
        
        return {
            "success": True,
            "message": f"Commitment added for {client_name}"
        }
    
    async def _check_renewals(self, days_ahead: int = None) -> Dict[str, Any]:
        """Check for upcoming contract renewals"""
        
        days_ahead = days_ahead or RENEWAL_ALERT_DAYS
        today = date.today()
        alert_date = today + timedelta(days=days_ahead)
        
        clients = await self._load_all_clients()
        renewals = []
        
        for client in clients:
            if client.get("type") != "client":
                continue
            
            if not client.get("contract_end"):
                continue
            
            end_date = datetime.fromisoformat(client["contract_end"]).date()
            if today <= end_date <= alert_date:
                days_until = (end_date - today).days
                renewals.append({
                    "client_name": client["name"],
                    "contract_end": client["contract_end"],
                    "days_until": days_until,
                    "health_score": client.get("health_score", 0)
                })
        
        # Sort by days until expiry
        renewals.sort(key=lambda r: r["days_until"])
        
        return {
            "success": True,
            "count": len(renewals),
            "renewals": renewals
        }
    
    async def _get_client_health(self, min_score: float = None) -> Dict[str, Any]:
        """Get relationship health scores"""
        
        clients = await self._load_all_clients()
        health_report = []
        
        for client in clients:
            if client.get("type") != "client":
                continue
            
            score = client.get("health_score", 0)
            
            if min_score and score >= min_score:
                continue
            
            health_report.append({
                "client_name": client["name"],
                "health_score": score,
                "last_meeting": client["meetings"][-1]["date"] if client.get("meetings") else None,
                "open_commitments": sum(
                    1 for c in client.get("commitments", [])
                    if c.get("status") == "open"
                )
            })
        
        # Sort by health score (lowest first)
        health_report.sort(key=lambda h: h["health_score"])
        
        return {
            "success": True,
            "count": len(health_report),
            "clients": health_report
        }
    
    async def _update_health_score(
        self,
        client_name: str,
        score: float,
        notes: str = ""
    ) -> Dict[str, Any]:
        """Update client health score"""
        
        client = await self._load_client_by_name(client_name)
        if not client:
            return {"success": False, "error": f"Client '{client_name}' not found"}
        
        old_score = client.get("health_score", 0)
        client["health_score"] = score
        
        if "health_history" not in client:
            client["health_history"] = []
        
        client["health_history"].append({
            "date": datetime.now().isoformat(),
            "score": score,
            "notes": notes
        })
        
        client["updated_at"] = datetime.now().isoformat()
        
        await self._save_client(client)
        
        return {
            "success": True,
            "message": f"Health score updated: {old_score} → {score}",
            "new_score": score
        }
    
    async def _save_client(self, client: Dict[str, Any]):
        """Save client to YAML file"""
        
        # Determine storage path based on type
        if client.get("is_internal"):
            storage_path = PEOPLE_PATH
        else:
            storage_path = COMPANIES_PATH
        
        storage_path.mkdir(parents=True, exist_ok=True)
        
        client_file = storage_path / f"{client['client_id']}.yaml"
        with open(client_file, 'w') as f:
            yaml.safe_dump(client, f, default_flow_style=False, sort_keys=False)
        
        self.clients_cache[client['client_id']] = client
    
    async def _load_client_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Load client by name"""
        client_id = name.lower().replace(" ", "-")
        
        # Check cache first
        if client_id in self.clients_cache:
            return self.clients_cache[client_id]
        
        # Try both directories
        for path in [PEOPLE_PATH, COMPANIES_PATH]:
            client_file = path / f"{client_id}.yaml"
            if client_file.exists():
                with open(client_file, 'r') as f:
                    client = yaml.safe_load(f)
                self.clients_cache[client_id] = client
                return client
        
        return None
    
    async def _load_all_clients(self) -> List[Dict[str, Any]]:
        """Load all clients from YAML files"""
        clients = []
        
        for path in [PEOPLE_PATH, COMPANIES_PATH]:
            if not path.exists():
                continue
            
            for client_file in path.glob("*.yaml"):
                try:
                    with open(client_file, 'r') as f:
                        client = yaml.safe_load(f)
                        if client:
                            clients.append(client)
                except Exception:
                    continue
        
        return clients


async def main():
    """Run the client server"""
    client_server = ClientServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await client_server.server.run(
            read_stream,
            write_stream,
            client_server.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
