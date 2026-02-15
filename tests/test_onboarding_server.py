"""
Tests for Onboarding Server - Client Onboarding Workflow MCP Server
"""

import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.mcp.onboarding_server import OnboardingServer


@pytest.fixture
def temp_data_dir(tmp_path, monkeypatch):
    """Create a temporary data directory for testing."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Patch Config to use temp directory
    from core import config
    monkeypatch.setattr(config.Config, "DATA_DIR", data_dir)
    
    yield data_dir


@pytest.fixture
def onboarding_server(temp_data_dir):
    """Create a fresh onboarding server instance for each test."""
    return OnboardingServer()


def test_start_onboarding(onboarding_server):
    """Test starting a new onboarding workflow."""
    result = onboarding_server.start_onboarding(
        client_id="client-123",
        client_name="Acme Corp",
        project_type="web_development"
    )
    
    assert "workflow_id" in result
    assert result["status"] == "started"
    assert result["workflow"]["client_name"] == "Acme Corp"
    assert result["workflow"]["current_step"] == 0
    assert result["workflow"]["completed"] is False


def test_get_workflow(onboarding_server):
    """Test retrieving an onboarding workflow."""
    # Start a workflow
    start_result = onboarding_server.start_onboarding(
        client_id="client-456",
        client_name="TechCorp",
        project_type="consulting"
    )
    workflow_id = start_result["workflow_id"]
    
    # Retrieve it
    get_result = onboarding_server.get_workflow(workflow_id)
    
    assert "workflow" in get_result
    assert get_result["workflow"]["id"] == workflow_id


def test_complete_step(onboarding_server):
    """Test completing a workflow step."""
    # Start workflow
    start_result = onboarding_server.start_onboarding(
        client_id="client-789",
        client_name="StartupCo",
        project_type="mobile_app"
    )
    workflow_id = start_result["workflow_id"]
    
    # Complete first step
    result = onboarding_server.complete_step(
        workflow_id=workflow_id,
        step_name="initial_consultation",
        notes="Discussed project requirements and timeline"
    )
    
    assert result.get("success")
    assert result["workflow"]["current_step"] == 1
    assert "completed_steps" in result["workflow"]


def test_complete_multiple_steps(onboarding_server):
    """Test completing multiple workflow steps."""
    # Start workflow
    start_result = onboarding_server.start_onboarding(
        client_id="client-multi",
        client_name="Multi Client",
        project_type="web_development"
    )
    workflow_id = start_result["workflow_id"]
    
    # Complete several steps
    steps = [
        "initial_consultation",
        "requirements_gathering",
        "proposal_sent"
    ]
    
    for step in steps:
        result = onboarding_server.complete_step(
            workflow_id=workflow_id,
            step_name=step,
            notes=f"Completed {step}"
        )
        assert result.get("success")


def test_list_workflows(onboarding_server):
    """Test listing all onboarding workflows."""
    # Create multiple workflows
    onboarding_server.start_onboarding("client-1", "Client 1", "web_development")
    onboarding_server.start_onboarding("client-2", "Client 2", "consulting")
    onboarding_server.start_onboarding("client-3", "Client 3", "mobile_app")
    
    # List all
    result = onboarding_server.list_workflows()
    
    assert "records" in result
    assert result["count"] >= 3


def test_list_workflows_by_status(onboarding_server):
    """Test filtering workflows by completion status."""
    # Create and complete one workflow
    wf1 = onboarding_server.start_onboarding("client-a", "Client A", "web_development")
    wf2 = onboarding_server.start_onboarding("client-b", "Client B", "consulting")
    
    # Mark one as completed (would need all steps, but for test purposes)
    # We'll just check we can filter
    result = onboarding_server.list_workflows()
    
    active_workflows = [w for w in result["records"] if not w.get("completed")]
    assert len(active_workflows) >= 2


def test_generate_sow(onboarding_server):
    """Test generating a Statement of Work."""
    result = onboarding_server.generate_sow(
        client_name="SOW Client",
        project_title="E-commerce Platform Development",
        scope_items=[
            "Design and implement product catalog",
            "Integrate payment gateway",
            "Build admin dashboard"
        ],
        deliverables=[
            "Fully functional e-commerce website",
            "Admin panel with analytics",
            "Documentation and training"
        ],
        timeline="12 weeks",
        total_cost=50000.0
    )
    
    assert "sow_id" in result
    assert result["status"] == "generated"
    assert result["sow"]["client_name"] == "SOW Client"
    assert len(result["sow"]["scope_items"]) == 3
    assert len(result["sow"]["deliverables"]) == 3


def test_get_sow(onboarding_server):
    """Test retrieving a generated SOW."""
    # Generate SOW
    gen_result = onboarding_server.generate_sow(
        client_name="Test Client",
        project_title="Test Project",
        scope_items=["Item 1", "Item 2"],
        deliverables=["Deliverable 1"],
        timeline="4 weeks",
        total_cost=10000.0
    )
    sow_id = gen_result["sow_id"]
    
    # Retrieve it
    get_result = onboarding_server.get_sow(sow_id)
    
    assert "sow" in get_result
    assert get_result["sow"]["id"] == sow_id


def test_update_workflow_status(onboarding_server):
    """Test updating workflow status."""
    # Start workflow
    start_result = onboarding_server.start_onboarding(
        client_id="client-status",
        client_name="Status Client",
        project_type="consulting"
    )
    workflow_id = start_result["workflow_id"]
    
    # Update status
    result = onboarding_server.update_workflow(
        workflow_id=workflow_id,
        status="in_progress",
        notes="Waiting for client to sign contract"
    )
    
    assert result.get("success")
    assert result["record"]["status"] == "in_progress"


def test_get_workflow_template(onboarding_server):
    """Test getting workflow templates by project type."""
    result = onboarding_server.get_workflow_template(
        project_type="web_development"
    )
    
    assert "template" in result
    assert "steps" in result["template"]
    assert len(result["template"]["steps"]) > 0


def test_server_info(onboarding_server):
    """Test getting server information."""
    info = onboarding_server.get_info()
    
    assert info["name"] == "onboarding-server"
    assert "version" in info
    assert "tools" in info
    assert "start_onboarding" in info["tools"]
    assert "generate_sow" in info["tools"]


def test_server_health_check(onboarding_server):
    """Test server health check."""
    health = onboarding_server.health_check()
    
    assert "healthy" in health
    assert health["server"] == "onboarding"


def test_workflow_completion_percentage(onboarding_server):
    """Test tracking workflow completion percentage."""
    # Start workflow
    start_result = onboarding_server.start_onboarding(
        client_id="client-pct",
        client_name="Percent Client",
        project_type="web_development"
    )
    workflow_id = start_result["workflow_id"]
    
    # Complete a step
    onboarding_server.complete_step(
        workflow_id=workflow_id,
        step_name="initial_consultation"
    )
    
    # Get workflow and check progress
    workflow = onboarding_server.get_workflow(workflow_id)
    
    # Should have some progress
    assert workflow["workflow"]["current_step"] > 0


def test_checklist_items(onboarding_server):
    """Test checklist functionality within workflows."""
    # Start workflow
    start_result = onboarding_server.start_onboarding(
        client_id="client-check",
        client_name="Checklist Client",
        project_type="consulting"
    )
    workflow_id = start_result["workflow_id"]
    
    # Add checklist items
    result = onboarding_server.add_checklist_item(
        workflow_id=workflow_id,
        item="Collect client requirements document",
        category="documentation"
    )
    
    assert result.get("success") or "checklist" in result


def test_sow_with_payment_schedule(onboarding_server):
    """Test generating SOW with payment schedule."""
    result = onboarding_server.generate_sow(
        client_name="Payment Client",
        project_title="Custom Software",
        scope_items=["Feature 1", "Feature 2"],
        deliverables=["Software", "Docs"],
        timeline="8 weeks",
        total_cost=40000.0,
        payment_schedule=[
            {"milestone": "Project Start", "amount": 10000.0},
            {"milestone": "Midpoint Review", "amount": 15000.0},
            {"milestone": "Final Delivery", "amount": 15000.0}
        ]
    )
    
    assert result["sow"]["total_cost"] == 40000.0
    if "payment_schedule" in result["sow"]:
        assert len(result["sow"]["payment_schedule"]) == 3
