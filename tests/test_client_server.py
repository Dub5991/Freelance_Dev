"""
Tests for Client Server - CRM MCP Server
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.mcp.client_server import ClientServer


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
def client_server(temp_data_dir):
    """Create a fresh client server instance for each test."""
    return ClientServer()


def test_create_client_basic(client_server):
    """Test creating a basic client."""
    result = client_server.create_client(
        name="John Doe",
        email="john@example.com",
        company="Acme Corp",
        phone="+1-555-123-4567"
    )
    
    assert "client_id" in result
    assert result["status"] == "created"
    assert result["client"]["name"] == "John Doe"
    assert result["client"]["email"] == "john@example.com"
    assert result["client"]["company"] == "Acme Corp"
    assert result["client"]["status"] == "active"
    assert result["client"]["health_score"] == 100


def test_create_client_invalid_email(client_server):
    """Test that invalid email is rejected."""
    result = client_server.create_client(
        name="Test Client",
        email="invalid-email"
    )
    
    assert "error" in result
    assert "invalid email" in result["error"].lower()


def test_create_client_duplicate_email(client_server):
    """Test that duplicate emails are not allowed."""
    # Create first client
    client_server.create_client(
        name="Client One",
        email="duplicate@example.com"
    )
    
    # Try to create duplicate
    result = client_server.create_client(
        name="Client Two",
        email="duplicate@example.com"
    )
    
    assert "error" in result
    assert "already exists" in result["error"].lower()


def test_get_client(client_server):
    """Test retrieving a client by ID."""
    # Create a client
    create_result = client_server.create_client(
        name="Jane Smith",
        email="jane@example.com"
    )
    client_id = create_result["client_id"]
    
    # Retrieve the client
    get_result = client_server.get_client(client_id)
    
    assert "client" in get_result
    assert get_result["client"]["name"] == "Jane Smith"
    assert get_result["client"]["id"] == client_id


def test_get_client_not_found(client_server):
    """Test retrieving non-existent client."""
    result = client_server.get_client("client-nonexistent")
    
    assert "error" in result


def test_list_clients(client_server):
    """Test listing all clients."""
    # Create multiple clients
    client_server.create_client("Client 1", "c1@example.com")
    client_server.create_client("Client 2", "c2@example.com")
    client_server.create_client("Client 3", "c3@example.com")
    
    # List all clients
    result = client_server.list_clients()
    
    assert "records" in result
    assert result["count"] == 3


def test_update_client(client_server):
    """Test updating client information."""
    # Create a client
    create_result = client_server.create_client(
        name="Original Name",
        email="original@example.com"
    )
    client_id = create_result["client_id"]
    
    # Update the client
    update_result = client_server.update_client(
        client_id=client_id,
        name="Updated Name",
        phone="+1-555-999-8888"
    )
    
    assert update_result.get("success")
    assert update_result["record"]["name"] == "Updated Name"
    assert update_result["record"]["phone"] == "+1-555-999-8888"


def test_log_communication(client_server):
    """Test logging client communication."""
    # Create a client
    create_result = client_server.create_client(
        name="Test Client",
        email="test@example.com"
    )
    client_id = create_result["client_id"]
    
    # Log communication
    result = client_server.log_communication(
        client_id=client_id,
        communication_type="email",
        subject="Project Update",
        notes="Sent weekly status update",
        direction="outbound"
    )
    
    assert "communication_id" in result
    assert result.get("status") == "logged"


def test_schedule_meeting(client_server):
    """Test scheduling a meeting."""
    # Create a client
    create_result = client_server.create_client(
        name="Meeting Client",
        email="meeting@example.com"
    )
    client_id = create_result["client_id"]
    
    # Schedule meeting
    result = client_server.schedule_meeting(
        client_id=client_id,
        title="Project Kickoff",
        scheduled_time="2024-06-15T10:00:00",
        duration_minutes=60,
        agenda="Discuss project scope and timeline"
    )
    
    assert "meeting_id" in result
    assert result.get("status") == "scheduled"


def test_log_meeting_notes(client_server):
    """Test logging notes from a completed meeting."""
    # Create client and schedule meeting
    create_result = client_server.create_client(
        name="Client",
        email="client@example.com"
    )
    client_id = create_result["client_id"]
    
    meeting_result = client_server.schedule_meeting(
        client_id=client_id,
        title="Review Meeting",
        scheduled_time="2024-06-15T14:00:00"
    )
    meeting_id = meeting_result["meeting_id"]
    
    # Log notes
    result = client_server.log_meeting_notes(
        meeting_id=meeting_id,
        notes="Reviewed Q2 deliverables. Client is satisfied.",
        action_items=["Send final invoice", "Schedule follow-up"],
        attendees=["John Doe", "Jane Smith"]
    )
    
    assert result.get("success")
    assert result["record"]["status"] == "completed"


def test_calculate_health_score(client_server):
    """Test calculating client health score."""
    # Create a client
    create_result = client_server.create_client(
        name="Health Test Client",
        email="health@example.com"
    )
    client_id = create_result["client_id"]
    
    # Calculate health score
    result = client_server.calculate_health_score(client_id)
    
    assert "health_score" in result
    assert 0 <= result["health_score"] <= 100
    assert "factors" in result


def test_get_client_summary(client_server):
    """Test getting a comprehensive client summary."""
    # Create client with activity
    create_result = client_server.create_client(
        name="Summary Client",
        email="summary@example.com"
    )
    client_id = create_result["client_id"]
    
    # Add some activity
    client_server.log_communication(
        client_id=client_id,
        communication_type="email",
        subject="Test",
        direction="outbound"
    )
    
    # Get summary
    result = client_server.get_client_summary(client_id)
    
    assert "client" in result
    assert "communications" in result
    assert "meetings" in result
    assert "health_score" in result


def test_server_info(client_server):
    """Test getting server information."""
    info = client_server.get_info()
    
    assert info["name"] == "client-server"
    assert "version" in info
    assert "tools" in info
    assert "create_client" in info["tools"]
    assert "calculate_health_score" in info["tools"]


def test_server_health_check(client_server):
    """Test server health check."""
    health = client_server.health_check()
    
    assert "healthy" in health
    assert health["server"] == "client"
