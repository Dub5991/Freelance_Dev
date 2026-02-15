"""
Onboarding Server - MCP Server for Setup Wizard

Full async implementation for:
- Session state, validation, resume capability
- Collects: LLC name, owner name, email domain, billing rates, Stripe readiness, strategic pillars
- Creates vault folder structure
"""

import asyncio
import os
from datetime import datetime
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
SYSTEM_PATH = Path(VAULT_PATH) / "06-Resources" / "System"
ONBOARDING_STATE_FILE = SYSTEM_PATH / "onboarding_state.yaml"


class OnboardingServer:
    """Async MCP Server for onboarding and setup"""
    
    def __init__(self):
        self.server = Server("onboarding-server")
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup all tool handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="start_onboarding",
                    description="Start or resume the onboarding process",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="submit_step",
                    description="Submit data for an onboarding step",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "step": {
                                "type": "string",
                                "enum": [
                                    "llc_info", "owner_info", "billing_rates",
                                    "stripe_setup", "strategic_pillars"
                                ],
                                "description": "Which step to submit"
                            },
                            "data": {
                                "type": "object",
                                "description": "Step data as key-value pairs"
                            }
                        },
                        "required": ["step", "data"]
                    }
                ),
                Tool(
                    name="get_onboarding_status",
                    description="Get current onboarding status",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="complete_onboarding",
                    description="Finalize onboarding and create vault structure",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Route tool calls to appropriate handlers"""
            
            if name == "start_onboarding":
                result = await self._start_onboarding()
                return [TextContent(type="text", text=str(result))]
            
            elif name == "submit_step":
                result = await self._submit_step(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "get_onboarding_status":
                result = await self._get_onboarding_status()
                return [TextContent(type="text", text=str(result))]
            
            elif name == "complete_onboarding":
                result = await self._complete_onboarding()
                return [TextContent(type="text", text=str(result))]
            
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def _start_onboarding(self) -> Dict[str, Any]:
        """Start or resume onboarding"""
        
        state = await self._load_state()
        
        if state and state.get("completed"):
            return {
                "success": False,
                "error": "Onboarding already completed",
                "completed_at": state.get("completed_at")
            }
        
        if not state:
            # Initialize new onboarding session
            state = {
                "started_at": datetime.now().isoformat(),
                "completed": False,
                "steps": {
                    "llc_info": {"completed": False},
                    "owner_info": {"completed": False},
                    "billing_rates": {"completed": False},
                    "stripe_setup": {"completed": False},
                    "strategic_pillars": {"completed": False}
                }
            }
            await self._save_state(state)
        
        # Determine current step
        current_step = None
        for step, info in state["steps"].items():
            if not info["completed"]:
                current_step = step
                break
        
        return {
            "success": True,
            "message": "Onboarding started" if not state.get("resumed") else "Onboarding resumed",
            "current_step": current_step,
            "progress": self._calculate_progress(state)
        }
    
    async def _submit_step(self, step: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit data for an onboarding step"""
        
        state = await self._load_state()
        if not state:
            return {"success": False, "error": "Onboarding not started. Call start_onboarding first."}
        
        # Validate step data
        validation = self._validate_step_data(step, data)
        if not validation["valid"]:
            return {
                "success": False,
                "error": validation["error"],
                "required_fields": validation.get("required_fields", [])
            }
        
        # Save step data
        state["steps"][step]["completed"] = True
        state["steps"][step]["data"] = data
        state["steps"][step]["completed_at"] = datetime.now().isoformat()
        
        await self._save_state(state)
        
        # Determine next step
        next_step = None
        for s, info in state["steps"].items():
            if not info["completed"]:
                next_step = s
                break
        
        all_complete = all(s["completed"] for s in state["steps"].values())
        
        return {
            "success": True,
            "message": f"Step '{step}' completed",
            "next_step": next_step,
            "all_steps_complete": all_complete,
            "progress": self._calculate_progress(state)
        }
    
    async def _get_onboarding_status(self) -> Dict[str, Any]:
        """Get current onboarding status"""
        
        state = await self._load_state()
        
        if not state:
            return {
                "success": True,
                "status": "not_started",
                "message": "Onboarding not started. Call start_onboarding to begin."
            }
        
        if state.get("completed"):
            return {
                "success": True,
                "status": "completed",
                "completed_at": state.get("completed_at"),
                "vault_created": state.get("vault_created", False)
            }
        
        steps_status = []
        for step, info in state["steps"].items():
            steps_status.append({
                "step": step,
                "completed": info["completed"],
                "completed_at": info.get("completed_at")
            })
        
        return {
            "success": True,
            "status": "in_progress",
            "started_at": state.get("started_at"),
            "progress": self._calculate_progress(state),
            "steps": steps_status
        }
    
    async def _complete_onboarding(self) -> Dict[str, Any]:
        """Finalize onboarding and create vault structure"""
        
        state = await self._load_state()
        
        if not state:
            return {"success": False, "error": "Onboarding not started"}
        
        if state.get("completed"):
            return {"success": False, "error": "Onboarding already completed"}
        
        # Check all steps are complete
        if not all(s["completed"] for s in state["steps"].values()):
            incomplete = [s for s, info in state["steps"].items() if not info["completed"]]
            return {
                "success": False,
                "error": "Not all steps completed",
                "incomplete_steps": incomplete
            }
        
        # Create vault folder structure
        vault_structure = [
            "00-Inbox",
            "01-Quarter_Goals",
            "02-Week_Priorities",
            "03-Tasks",
            "04-Projects",
            "05-Areas/People",
            "05-Areas/Companies",
            "05-Areas/Finance/invoices",
            "05-Areas/Finance/expenses",
            "05-Areas/Finance/tax",
            "05-Areas/Business_Dev",
            "06-Resources/System",
            "06-Resources/Templates",
            "07-Archives"
        ]
        
        created_folders = []
        for folder in vault_structure:
            folder_path = Path(VAULT_PATH) / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            created_folders.append(str(folder_path))
        
        # Create .env file from collected data
        env_data = self._generate_env_file(state)
        env_file = Path.cwd() / ".env"
        
        if not env_file.exists():
            with open(env_file, 'w') as f:
                f.write(env_data)
        
        # Mark as completed
        state["completed"] = True
        state["completed_at"] = datetime.now().isoformat()
        state["vault_created"] = True
        state["env_created"] = not env_file.exists()
        
        await self._save_state(state)
        
        return {
            "success": True,
            "message": "Onboarding completed successfully!",
            "folders_created": len(created_folders),
            "env_file_created": state["env_created"],
            "next_steps": [
                "1. Review and update your .env file with API keys",
                "2. Run 'pip install -r requirements.txt' to install dependencies",
                "3. Configure your MCP client with the servers",
                "4. Start using the system with Claude!"
            ]
        }
    
    def _validate_step_data(self, step: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate step data"""
        
        validations = {
            "llc_info": {
                "required": ["llc_name", "ein"],
                "validators": {
                    "ein": lambda v: len(v.replace("-", "")) == 9
                }
            },
            "owner_info": {
                "required": ["owner_name", "email"],
                "validators": {
                    "email": lambda v: "@" in v
                }
            },
            "billing_rates": {
                "required": ["default_hourly_rate"],
                "validators": {
                    "default_hourly_rate": lambda v: isinstance(v, (int, float)) and v > 0
                }
            },
            "stripe_setup": {
                "required": ["stripe_ready"],
                "validators": {}
            },
            "strategic_pillars": {
                "required": ["pillars"],
                "validators": {
                    "pillars": lambda v: isinstance(v, list) and len(v) > 0
                }
            }
        }
        
        if step not in validations:
            return {"valid": False, "error": f"Unknown step: {step}"}
        
        config = validations[step]
        
        # Check required fields
        missing = [f for f in config["required"] if f not in data]
        if missing:
            return {
                "valid": False,
                "error": f"Missing required fields: {', '.join(missing)}",
                "required_fields": config["required"]
            }
        
        # Run validators
        for field, validator in config.get("validators", {}).items():
            if field in data and not validator(data[field]):
                return {
                    "valid": False,
                    "error": f"Invalid value for {field}"
                }
        
        return {"valid": True}
    
    def _calculate_progress(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate onboarding progress"""
        total = len(state["steps"])
        completed = sum(1 for s in state["steps"].values() if s["completed"])
        percentage = int((completed / total) * 100)
        
        return {
            "total_steps": total,
            "completed_steps": completed,
            "percentage": percentage
        }
    
    def _generate_env_file(self, state: Dict[str, Any]) -> str:
        """Generate .env file content from onboarding data"""
        
        llc_info = state["steps"]["llc_info"]["data"]
        owner_info = state["steps"]["owner_info"]["data"]
        billing = state["steps"]["billing_rates"]["data"]
        stripe = state["steps"]["stripe_setup"]["data"]
        pillars = state["steps"]["strategic_pillars"]["data"]
        
        env_content = f"""# Generated by Freelance LLC OS Onboarding
# Generated at: {datetime.now().isoformat()}

# LLC Information
LLC_NAME="{llc_info.get('llc_name', '')}"
OWNER_NAME="{owner_info.get('owner_name', '')}"
OWNER_EMAIL="{owner_info.get('email', '')}"
LLC_EIN="{llc_info.get('ein', '')}"

# Billing Configuration
DEFAULT_HOURLY_RATE={billing.get('default_hourly_rate', 150)}

# Stripe Integration
# 🔴 YOUR ACTION NEEDED: Add your Stripe keys from dashboard.stripe.com
STRIPE_SECRET_KEY="sk_test_YOUR_KEY_HERE"
STRIPE_PUBLISHABLE_KEY="pk_test_YOUR_KEY_HERE"
STRIPE_WEBHOOK_SECRET="whsec_YOUR_SECRET_HERE"

# AI Model
CLAUDE_MODEL="claude-3-5-sonnet-20241022"

# Vault Path
VAULT_PATH="{VAULT_PATH}"

# Tax Configuration
QUARTERLY_TAX_RATE=0.25

# Strategic Pillars
STRATEGIC_PILLARS="{','.join(pillars.get('pillars', []))}"

# Notification Thresholds
RENEWAL_ALERT_DAYS=30
LOW_CLIENT_HEALTH_THRESHOLD=5
MAX_P0_TASKS=3
"""
        
        return env_content
    
    async def _save_state(self, state: Dict[str, Any]):
        """Save onboarding state"""
        SYSTEM_PATH.mkdir(parents=True, exist_ok=True)
        
        with open(ONBOARDING_STATE_FILE, 'w') as f:
            yaml.safe_dump(state, f, default_flow_style=False, sort_keys=False)
    
    async def _load_state(self) -> Optional[Dict[str, Any]]:
        """Load onboarding state"""
        if not ONBOARDING_STATE_FILE.exists():
            return None
        
        with open(ONBOARDING_STATE_FILE, 'r') as f:
            return yaml.safe_load(f)


async def main():
    """Run the onboarding server"""
    onboarding_server = OnboardingServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await onboarding_server.server.run(
            read_stream,
            write_stream,
            onboarding_server.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
