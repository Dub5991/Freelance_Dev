"""
Onboarding Server - Client Onboarding Workflow Management MCP Server

Features:
- Onboarding workflow/pipeline management
- Template-based onboarding checklists
- Contract generation and tracking
- Scope of work (SOW) creation
- Welcome packet generation
- Automated status updates
"""

from datetime import datetime, date
from typing import Optional, List, Dict
from ..config import Config
from ..utils import generate_id, format_date
from .base_server import BaseMCPServer


class OnboardingServer(BaseMCPServer):
    """Client onboarding workflow management server."""
    
    def __init__(self):
        super().__init__("onboarding")
        
        # Initialize collections
        if "onboarding_workflows" not in self._data:
            self._data["onboarding_workflows"] = {}
        
        if "templates" not in self._data:
            self._data["templates"] = {}
            self._initialize_templates()
        
        if "contracts" not in self._data:
            self._data["contracts"] = {}
    
    def get_info(self) -> dict:
        """Return server metadata."""
        return {
            "name": "onboarding-server",
            "version": "0.1.0",
            "description": "Client onboarding workflow MCP server",
            "tools": [
                "start_onboarding",
                "get_onboarding_status",
                "update_onboarding_step",
                "complete_onboarding",
                "create_contract",
                "get_contract",
                "sign_contract",
                "generate_scope_of_work",
                "send_welcome_packet",
                "list_onboarding_workflows"
            ]
        }
    
    def _initialize_templates(self) -> None:
        """Initialize default onboarding templates."""
        templates = self._get_collection("templates")
        
        if not templates:
            default_template = {
                "name": "Standard Client Onboarding",
                "description": "Standard onboarding workflow for new clients",
                "steps": [
                    {
                        "id": "initial_meeting",
                        "title": "Initial Discovery Meeting",
                        "description": "Schedule and conduct discovery meeting to understand client needs",
                        "order": 1,
                        "required": True
                    },
                    {
                        "id": "scope_of_work",
                        "title": "Create Scope of Work",
                        "description": "Draft detailed scope of work document",
                        "order": 2,
                        "required": True
                    },
                    {
                        "id": "send_proposal",
                        "title": "Send Proposal",
                        "description": "Send project proposal with pricing and timeline",
                        "order": 3,
                        "required": True
                    },
                    {
                        "id": "contract_creation",
                        "title": "Generate Contract",
                        "description": "Create and send service agreement",
                        "order": 4,
                        "required": True
                    },
                    {
                        "id": "contract_signed",
                        "title": "Contract Signed",
                        "description": "Obtain signed contract from client",
                        "order": 5,
                        "required": True
                    },
                    {
                        "id": "payment_setup",
                        "title": "Set Up Payment",
                        "description": "Set up payment method and send first invoice",
                        "order": 6,
                        "required": True
                    },
                    {
                        "id": "welcome_packet",
                        "title": "Send Welcome Packet",
                        "description": "Send welcome packet with project info and resources",
                        "order": 7,
                        "required": False
                    },
                    {
                        "id": "kickoff_meeting",
                        "title": "Project Kickoff",
                        "description": "Schedule and conduct project kickoff meeting",
                        "order": 8,
                        "required": True
                    }
                ]
            }
            
            template_id = "template-standard"
            templates[template_id] = {
                **default_template,
                "id": template_id,
                "created_at": datetime.now().isoformat()
            }
            
            self._set_collection("templates", templates)
            self._save_data()
    
    def start_onboarding(
        self,
        client_id: str,
        client_name: str,
        template_id: str = "template-standard",
        project_name: Optional[str] = None,
        notes: Optional[str] = None
    ) -> dict:
        """
        Start onboarding workflow for a new client.
        
        Args:
            client_id: Client identifier
            client_name: Client name
            template_id: Onboarding template to use
            project_name: Project name
            notes: Additional notes
        
        Returns:
            Onboarding workflow record
        """
        # Get template
        templates = self._get_collection("templates")
        if template_id not in templates:
            return {"error": f"Template '{template_id}' not found"}
        
        template = templates[template_id]
        
        # Generate workflow ID
        workflow_id = generate_id("onboarding")
        
        # Initialize steps from template
        steps = []
        for step_template in template.get("steps", []):
            steps.append({
                **step_template,
                "status": "pending",
                "completed_date": None,
                "notes": ""
            })
        
        workflow_data = {
            "client_id": client_id,
            "client_name": client_name,
            "project_name": project_name or f"{client_name} Project",
            "template_id": template_id,
            "template_name": template.get("name"),
            "status": "in_progress",
            "current_step": 0,
            "steps": steps,
            "started_date": date.today().isoformat(),
            "completed_date": None,
            "notes": notes or ""
        }
        
        result = self._create_record("onboarding_workflows", workflow_id, workflow_data)
        
        if result.get("success"):
            self.logger.info(f"Started onboarding for {client_name} ({workflow_id})")
            return {
                "workflow_id": workflow_id,
                "status": "started",
                "workflow": result["record"]
            }
        
        return result
    
    def get_onboarding_status(self, workflow_id: str) -> dict:
        """
        Get onboarding workflow status.
        
        Args:
            workflow_id: Workflow identifier
        
        Returns:
            Workflow status with progress
        """
        result = self._read_record("onboarding_workflows", workflow_id)
        
        if result.get("success"):
            workflow = result["record"]
            steps = workflow.get("steps", [])
            
            # Calculate progress
            total_steps = len(steps)
            completed_steps = sum(1 for s in steps if s.get("status") == "completed")
            progress_percent = (completed_steps / total_steps * 100) if total_steps > 0 else 0
            
            # Find next pending step
            next_step = None
            for step in steps:
                if step.get("status") == "pending":
                    next_step = step
                    break
            
            return {
                "workflow": workflow,
                "progress": {
                    "completed_steps": completed_steps,
                    "total_steps": total_steps,
                    "percent_complete": round(progress_percent, 1),
                    "next_step": next_step
                }
            }
        
        return result
    
    def update_onboarding_step(
        self,
        workflow_id: str,
        step_id: str,
        status: str = "completed",
        notes: Optional[str] = None
    ) -> dict:
        """
        Update status of an onboarding step.
        
        Args:
            workflow_id: Workflow identifier
            step_id: Step identifier
            status: New status (pending, in_progress, completed, skipped)
            notes: Step notes
        
        Returns:
            Updated workflow
        """
        workflow_result = self._read_record("onboarding_workflows", workflow_id)
        if not workflow_result.get("success"):
            return workflow_result
        
        workflow = workflow_result["record"]
        steps = workflow.get("steps", [])
        
        # Find and update step
        step_found = False
        for step in steps:
            if step.get("id") == step_id:
                step["status"] = status
                if notes:
                    step["notes"] = notes
                if status == "completed":
                    step["completed_date"] = date.today().isoformat()
                step_found = True
                break
        
        if not step_found:
            return {"error": f"Step '{step_id}' not found in workflow"}
        
        # Update current step index
        for i, step in enumerate(steps):
            if step.get("status") == "pending":
                workflow["current_step"] = i
                break
        
        # Check if all required steps are complete
        required_steps = [s for s in steps if s.get("required")]
        all_required_complete = all(s.get("status") == "completed" for s in required_steps)
        
        if all_required_complete and workflow.get("status") != "completed":
            workflow["status"] = "ready_to_complete"
        
        result = self._update_record("onboarding_workflows", workflow_id, {
            "steps": steps,
            "current_step": workflow.get("current_step"),
            "status": workflow.get("status")
        })
        
        if result.get("success"):
            return {
                "workflow_id": workflow_id,
                "step_id": step_id,
                "status": "updated",
                "workflow": result["record"]
            }
        
        return result
    
    def complete_onboarding(
        self,
        workflow_id: str,
        notes: Optional[str] = None
    ) -> dict:
        """
        Mark onboarding workflow as completed.
        
        Args:
            workflow_id: Workflow identifier
            notes: Completion notes
        
        Returns:
            Completed workflow
        """
        workflow_result = self._read_record("onboarding_workflows", workflow_id)
        if not workflow_result.get("success"):
            return workflow_result
        
        workflow = workflow_result["record"]
        
        # Check if all required steps are completed
        steps = workflow.get("steps", [])
        required_steps = [s for s in steps if s.get("required")]
        incomplete_required = [s for s in required_steps if s.get("status") != "completed"]
        
        if incomplete_required:
            return {
                "error": "Cannot complete onboarding. Required steps incomplete",
                "incomplete_steps": [s.get("title") for s in incomplete_required]
            }
        
        updates = {
            "status": "completed",
            "completed_date": date.today().isoformat()
        }
        
        if notes:
            updates["completion_notes"] = notes
        
        result = self._update_record("onboarding_workflows", workflow_id, updates)
        
        if result.get("success"):
            self.logger.info(f"Completed onboarding workflow {workflow_id}")
            return {
                "workflow_id": workflow_id,
                "status": "completed",
                "workflow": result["record"]
            }
        
        return result
    
    def create_contract(
        self,
        client_id: str,
        client_name: str,
        contract_type: str,
        terms: Dict[str, any],
        template: Optional[str] = None
    ) -> dict:
        """
        Create a contract for a client.
        
        Args:
            client_id: Client identifier
            client_name: Client name
            contract_type: Contract type (service_agreement, nda, msa, sow, other)
            terms: Contract terms dictionary
            template: Contract template to use
        
        Returns:
            Contract record
        """
        contract_id = generate_id("contract")
        
        contract_data = {
            "client_id": client_id,
            "client_name": client_name,
            "type": contract_type,
            "terms": terms,
            "template": template,
            "status": "draft",
            "created_date": date.today().isoformat(),
            "sent_date": None,
            "signed_date": None,
            "signed_by": None,
            "expiration_date": terms.get("expiration_date"),
            "auto_renew": terms.get("auto_renew", False)
        }
        
        result = self._create_record("contracts", contract_id, contract_data)
        
        if result.get("success"):
            return {
                "contract_id": contract_id,
                "status": "created",
                "contract": result["record"]
            }
        
        return result
    
    def get_contract(self, contract_id: str) -> dict:
        """
        Get contract by ID.
        
        Args:
            contract_id: Contract identifier
        
        Returns:
            Contract details
        """
        result = self._read_record("contracts", contract_id)
        
        if result.get("success"):
            return {"contract": result["record"]}
        
        return result
    
    def sign_contract(
        self,
        contract_id: str,
        signed_by: str,
        signature_method: str = "electronic"
    ) -> dict:
        """
        Mark contract as signed.
        
        Args:
            contract_id: Contract identifier
            signed_by: Name of person who signed
            signature_method: Signature method (electronic, wet_signature)
        
        Returns:
            Updated contract
        """
        updates = {
            "status": "signed",
            "signed_date": date.today().isoformat(),
            "signed_by": signed_by,
            "signature_method": signature_method
        }
        
        result = self._update_record("contracts", contract_id, updates)
        
        if result.get("success"):
            return {
                "contract_id": contract_id,
                "status": "signed",
                "contract": result["record"]
            }
        
        return result
    
    def generate_scope_of_work(
        self,
        client_name: str,
        project_name: str,
        objectives: List[str],
        deliverables: List[Dict[str, str]],
        timeline: str,
        budget: Optional[float] = None,
        assumptions: Optional[List[str]] = None,
        exclusions: Optional[List[str]] = None
    ) -> dict:
        """
        Generate a scope of work document.
        
        Args:
            client_name: Client name
            project_name: Project name
            objectives: Project objectives
            deliverables: List of deliverables with descriptions
            timeline: Project timeline
            budget: Project budget
            assumptions: Project assumptions
            exclusions: Out of scope items
        
        Returns:
            Scope of work document
        """
        sow = {
            "document_type": "scope_of_work",
            "client_name": client_name,
            "project_name": project_name,
            "date": date.today().isoformat(),
            "llc_name": Config.LLC_NAME,
            "sections": {
                "objectives": objectives,
                "deliverables": deliverables,
                "timeline": timeline,
                "budget": budget,
                "assumptions": assumptions or [],
                "exclusions": exclusions or []
            },
            "approval": {
                "status": "pending",
                "approved_by": None,
                "approval_date": None
            }
        }
        
        return {
            "status": "generated",
            "scope_of_work": sow,
            "next_steps": [
                "Review SOW with client",
                "Incorporate feedback",
                "Get client approval",
                "Convert to contract"
            ]
        }
    
    def send_welcome_packet(
        self,
        workflow_id: str,
        packet_contents: Optional[Dict[str, str]] = None
    ) -> dict:
        """
        Send welcome packet to client.
        
        Args:
            workflow_id: Onboarding workflow identifier
            packet_contents: Custom packet contents
        
        Returns:
            Welcome packet info
        """
        workflow_result = self._read_record("onboarding_workflows", workflow_id)
        if not workflow_result.get("success"):
            return workflow_result
        
        workflow = workflow_result["record"]
        
        # Default welcome packet contents
        default_contents = {
            "welcome_letter": "Welcome to working with us!",
            "project_overview": f"Project: {workflow.get('project_name')}",
            "communication_guide": "How we communicate and collaborate",
            "timeline": "Project timeline and milestones",
            "contact_info": f"Primary contact: {Config.LLC_NAME}",
            "resources": "Links to project resources and tools"
        }
        
        contents = packet_contents or default_contents
        
        # Update workflow step
        self.update_onboarding_step(workflow_id, "welcome_packet", "completed")
        
        return {
            "workflow_id": workflow_id,
            "status": "sent",
            "packet_contents": contents,
            "sent_date": date.today().isoformat()
        }
    
    def list_onboarding_workflows(
        self,
        status: Optional[str] = None,
        client_id: Optional[str] = None
    ) -> dict:
        """
        List onboarding workflows.
        
        Args:
            status: Filter by status
            client_id: Filter by client
        
        Returns:
            List of workflows
        """
        def filter_func(workflow: dict) -> bool:
            if status and workflow.get("status") != status:
                return False
            if client_id and workflow.get("client_id") != client_id:
                return False
            return True
        
        result = self._list_records(
            "onboarding_workflows",
            filter_func,
            sort_key="started_date",
            reverse=True
        )
        
        if result.get("success"):
            workflows = result["records"]
            
            summary = {
                "total": len(workflows),
                "by_status": {}
            }
            
            for workflow in workflows:
                wf_status = workflow.get("status", "unknown")
                summary["by_status"][wf_status] = summary["by_status"].get(wf_status, 0) + 1
            
            return {
                "workflows": workflows,
                "summary": summary
            }
        
        return result


# Standalone functions for MCP tool interface
_server_instance = None

def _get_server() -> OnboardingServer:
    """Get or create server instance."""
    global _server_instance
    if _server_instance is None:
        _server_instance = OnboardingServer()
    return _server_instance


def start_onboarding(**kwargs) -> dict:
    """Start onboarding workflow."""
    return _get_server().start_onboarding(**kwargs)


def get_onboarding_status(workflow_id: str) -> dict:
    """Get onboarding status."""
    return _get_server().get_onboarding_status(workflow_id)


def update_onboarding_step(**kwargs) -> dict:
    """Update onboarding step."""
    return _get_server().update_onboarding_step(**kwargs)


def complete_onboarding(**kwargs) -> dict:
    """Complete onboarding."""
    return _get_server().complete_onboarding(**kwargs)


def create_contract(**kwargs) -> dict:
    """Create contract."""
    return _get_server().create_contract(**kwargs)


def get_contract(contract_id: str) -> dict:
    """Get contract."""
    return _get_server().get_contract(contract_id)


def sign_contract(**kwargs) -> dict:
    """Sign contract."""
    return _get_server().sign_contract(**kwargs)


def generate_scope_of_work(**kwargs) -> dict:
    """Generate scope of work."""
    return _get_server().generate_scope_of_work(**kwargs)


def send_welcome_packet(**kwargs) -> dict:
    """Send welcome packet."""
    return _get_server().send_welcome_packet(**kwargs)


def list_onboarding_workflows(**kwargs) -> dict:
    """List onboarding workflows."""
    return _get_server().list_onboarding_workflows(**kwargs)


def get_server_info() -> dict:
    """Get server info."""
    return _get_server().get_info()


if __name__ == "__main__":
    server = OnboardingServer()
    print("Onboarding Server - Client Onboarding Workflow MCP Server")
    print(f"Data file: {server.data_path}")
    info = server.get_info()
    print(f"Available tools: {', '.join(info['tools'])}")
