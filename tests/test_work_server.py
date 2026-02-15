"""
Tests for Work Server - Task Management MCP Server
"""

import os
import pytest
import tempfile
import yaml
from datetime import date
from pathlib import Path

# Import work server functions
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.mcp import work_server


@pytest.fixture
def temp_vault(monkeypatch, tmp_path):
    """Create a temporary vault directory for testing."""
    vault_path = tmp_path / "test_vault"
    vault_path.mkdir()
    
    # Set environment variable
    monkeypatch.setenv("VAULT_PATH", str(vault_path))
    
    # Update work_server module variables
    work_server.VAULT_PATH = str(vault_path)
    work_server.TASKS_DIR = os.path.join(str(vault_path), "03-Tasks")
    work_server.TASKS_FILE = os.path.join(work_server.TASKS_DIR, "tasks.yaml")
    work_server.HOURS_FILE = os.path.join(work_server.TASKS_DIR, "hours.yaml")
    
    # Ensure directories exist
    work_server._ensure_dirs()
    
    yield vault_path
    
    # Cleanup is automatic with tmp_path


@pytest.fixture
def clean_tasks(temp_vault):
    """Ensure clean task storage for each test."""
    tasks_file = work_server.TASKS_FILE
    hours_file = work_server.HOURS_FILE
    
    # Clear any existing data
    if os.path.exists(tasks_file):
        os.remove(tasks_file)
    if os.path.exists(hours_file):
        os.remove(hours_file)
    
    yield
    
    # Cleanup
    if os.path.exists(tasks_file):
        os.remove(tasks_file)
    if os.path.exists(hours_file):
        os.remove(hours_file)


def test_create_task_basic(clean_tasks):
    """Test creating a basic task."""
    result = work_server.create_task(
        title="Test API Integration",
        priority="P1",
        billable=True,
        client="AcmeCorp",
        estimated_hours=10.0
    )
    
    assert "task_id" in result
    assert result["status"] == "created"
    assert result["task"]["title"] == "Test API Integration"
    assert result["task"]["priority"] == "P1"
    assert result["task"]["billable"] is True
    assert result["task"]["client"] == "AcmeCorp"
    assert result["task"]["tag"] == "[BILLABLE]"


def test_create_task_requires_client_for_billable(clean_tasks):
    """Test that billable tasks require a client."""
    result = work_server.create_task(
        title="Test Task",
        billable=True
    )
    
    assert "error" in result
    assert "client" in result["error"].lower()


def test_create_task_p0_limit(clean_tasks):
    """Test that P0 tasks are limited to 3 active."""
    # Create 3 P0 tasks successfully
    for i in range(3):
        result = work_server.create_task(
            title=f"P0 Task {i+1}",
            priority="P0",
            billable=False
        )
        assert result["status"] == "created"
    
    # Fourth P0 task should fail
    result = work_server.create_task(
        title="P0 Task 4",
        priority="P0",
        billable=False
    )
    
    assert "error" in result
    assert "maximum" in result["error"].lower()


def test_create_task_duplicate_detection(clean_tasks):
    """Test duplicate task detection."""
    # Create first task
    work_server.create_task(
        title="Database Setup",
        client="TechCorp",
        billable=True
    )
    
    # Try to create duplicate
    result = work_server.create_task(
        title="Database Setup",
        client="TechCorp",
        billable=True
    )
    
    assert "error" in result
    assert "duplicate" in result["error"].lower()


def test_list_tasks_empty(clean_tasks):
    """Test listing tasks when none exist."""
    result = work_server.list_tasks()
    
    assert "tasks" in result
    assert "summary" in result
    assert result["summary"]["total"] == 0


def test_list_tasks_with_filters(clean_tasks):
    """Test listing tasks with various filters."""
    # Create multiple tasks
    work_server.create_task("Task 1", priority="P0", billable=True, client="ClientA")
    work_server.create_task("Task 2", priority="P1", billable=True, client="ClientB")
    work_server.create_task("Task 3", priority="P2", billable=False)
    
    # Filter by priority
    result = work_server.list_tasks(priority="P0")
    assert result["summary"]["total"] == 1
    
    # Filter by client
    result = work_server.list_tasks(client="ClientA")
    assert result["summary"]["total"] == 1
    
    # Filter by billable status
    result = work_server.list_tasks(billable=False)
    assert result["summary"]["total"] == 1


def test_log_hours(clean_tasks):
    """Test logging hours on a task."""
    # Create a task
    create_result = work_server.create_task(
        title="Development Work",
        billable=True,
        client="TestClient",
        estimated_hours=20.0
    )
    task_id = create_result["task_id"]
    
    # Log hours
    log_result = work_server.log_hours(
        task_id=task_id,
        hours=5.0,
        description="Implemented API endpoints"
    )
    
    assert "hours_logged" in log_result
    assert log_result["hours_logged"] == 5.0
    assert log_result["total_hours_on_task"] == 5.0
    assert log_result["remaining"] == 15.0


def test_log_hours_invalid_task(clean_tasks):
    """Test logging hours on non-existent task."""
    result = work_server.log_hours(
        task_id="task-99999999-999",
        hours=5.0
    )
    
    assert "error" in result
    assert "not found" in result["error"].lower()


def test_complete_task(clean_tasks):
    """Test completing a task."""
    # Create and complete a task
    create_result = work_server.create_task(
        title="Testing Task",
        billable=True,
        client="ClientX"
    )
    task_id = create_result["task_id"]
    
    complete_result = work_server.complete_task(
        task_id=task_id,
        notes="All tests passing"
    )
    
    assert complete_result["status"] == "completed"
    assert complete_result["task"]["status"] == "completed"
    assert complete_result["task"]["completed_at"] is not None
    assert "billable_summary" in complete_result


def test_complete_task_already_completed(clean_tasks):
    """Test completing an already completed task."""
    create_result = work_server.create_task(
        title="Task",
        billable=False
    )
    task_id = create_result["task_id"]
    
    # Complete once
    work_server.complete_task(task_id)
    
    # Try to complete again
    result = work_server.complete_task(task_id)
    
    assert "error" in result
    assert "already completed" in result["error"].lower()


def test_get_billable_summary_current_month(clean_tasks):
    """Test getting billable hours summary for current month."""
    # Create task and log hours
    create_result = work_server.create_task(
        title="Project Work",
        billable=True,
        client="ClientA",
        estimated_hours=40.0
    )
    task_id = create_result["task_id"]
    
    work_server.log_hours(task_id, 10.0, "Week 1 work")
    work_server.log_hours(task_id, 15.0, "Week 2 work")
    
    # Get summary
    summary = work_server.get_billable_summary(period="current_month")
    
    assert "total_billable_hours" in summary
    assert summary["total_billable_hours"] == 25.0
    assert "by_client" in summary
    assert "ClientA" in summary["by_client"]
    assert summary["by_client"]["ClientA"]["hours"] == 25.0


def test_get_billable_summary_by_client(clean_tasks):
    """Test filtering billable summary by client."""
    # Create tasks for different clients
    task1 = work_server.create_task("Task 1", billable=True, client="ClientA")
    task2 = work_server.create_task("Task 2", billable=True, client="ClientB")
    
    work_server.log_hours(task1["task_id"], 10.0)
    work_server.log_hours(task2["task_id"], 15.0)
    
    # Get summary for specific client
    summary = work_server.get_billable_summary(client="ClientA")
    
    assert summary["total_billable_hours"] == 10.0
    assert "ClientA" in summary["by_client"]
    assert "ClientB" not in summary["by_client"]


def test_update_task(clean_tasks):
    """Test updating task fields."""
    # Create a task
    create_result = work_server.create_task(
        title="Initial Title",
        priority="P2",
        billable=False
    )
    task_id = create_result["task_id"]
    
    # Update task
    update_result = work_server.update_task(
        task_id=task_id,
        priority="P1",
        description="Updated description",
        status="active"
    )
    
    assert update_result["status"] == "updated"
    assert update_result["task"]["priority"] == "P1"
    assert update_result["task"]["description"] == "Updated description"


def test_update_task_to_p0_respects_limit(clean_tasks):
    """Test that updating to P0 respects the 3-task limit."""
    # Create 3 P0 tasks
    for i in range(3):
        work_server.create_task(f"P0 Task {i+1}", priority="P0", billable=False)
    
    # Create a P1 task
    task_result = work_server.create_task("P1 Task", priority="P1", billable=False)
    
    # Try to promote to P0
    result = work_server.update_task(task_result["task_id"], priority="P0")
    
    assert "error" in result
    assert "max" in result["error"].lower()


def test_get_server_info():
    """Test getting server information."""
    info = work_server.get_server_info()
    
    assert info["name"] == "work-server"
    assert "version" in info
    assert "tools" in info
    assert "create_task" in info["tools"]
    assert "list_tasks" in info["tools"]
    assert "log_hours" in info["tools"]
