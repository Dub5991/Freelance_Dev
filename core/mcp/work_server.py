#!/usr/bin/env python3
"""
Work Server - Task Management MCP Server
Manages tasks with billable tracking, priority enforcement, and client alignment.

Features:
    - Unique task IDs (task-YYYYMMDD-XXX)
    - [BILLABLE] / [INTERNAL] tagging
    - Priority enforcement (max 3 P0s)
    - Billable hours tracking per client
    - YAML-based persistent storage
"""

import asyncio
import os
import yaml
from datetime import datetime, date
from typing import Optional
from pathlib import Path

# ---------- Configuration ----------

VAULT_PATH = os.environ.get("VAULT_PATH", os.path.expanduser("~/freelance-vault"))
TASKS_DIR = os.path.join(VAULT_PATH, "03-Tasks")
TASKS_FILE = os.path.join(TASKS_DIR, "tasks.yaml")
HOURS_FILE = os.path.join(TASKS_DIR, "hours.yaml")
MAX_P0_TASKS = 3

# ---------- Storage Helpers ----------

def _ensure_dirs():
    """Create storage directories if they don't exist."""
    os.makedirs(TASKS_DIR, exist_ok=True)


def _load_yaml(filepath: str) -> dict:
    """Load a YAML file, return empty dict if missing or invalid."""
    _ensure_dirs()
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                data = yaml.safe_load(f)
                return data if isinstance(data, dict) else {}
        except yaml.YAMLError:
            return {}
    return {}


def _save_yaml(filepath: str, data: dict):
    """Save data to a YAML file."""
    _ensure_dirs()
    with open(filepath, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def _load_tasks() -> dict:
    """Load all tasks from storage."""
    return _load_yaml(TASKS_FILE)


def _save_tasks(tasks: dict):
    """Save all tasks to storage."""
    _save_yaml(TASKS_FILE, tasks)


def _load_hours() -> dict:
    """Load all hour entries from storage."""
    return _load_yaml(HOURS_FILE)


def _save_hours(hours: dict):
    """Save all hour entries to storage."""
    _save_yaml(HOURS_FILE, hours)

# ---------- Task ID Generator ----------

def _generate_task_id() -> str:
    """Generate a unique task ID: task-YYYYMMDD-XXX."""
    today = date.today().strftime("%Y%m%d")
    tasks = _load_tasks()
    
    existing_today = [
        tid for tid in tasks.keys()
        if tid.startswith(f"task-{today}-")
    ]
    
    next_num = len(existing_today) + 1
    while True:
        task_id = f"task-{today}-{next_num:03d}"
        if task_id not in tasks:
            return task_id
        next_num += 1

# ---------- Validation ----------

def _count_p0_tasks(tasks: dict) -> int:
    """Count active P0 tasks."""
    return sum(
        1 for t in tasks.values()
        if t.get("priority") == "P0" and t.get("status") != "completed"
    )


def _is_duplicate(tasks: dict, title: str, client: Optional[str] = None) -> bool:
    """Check if a task with the same title and client already exists."""
    for t in tasks.values():
        if (t.get("title", "").lower() == title.lower() 
            and t.get("client") == client
            and t.get("status") != "completed"):
            return True
    return False

# ---------- MCP Tool Functions ----------

def create_task(
    title: str,
    priority: str = "P1",
    billable: bool = True,
    client: Optional[str] = None,
    description: str = "",
    pillar: Optional[str] = None,
    estimated_hours: float = 0.0
) -> dict:
    """
    Create a new task with unique ID and tracking metadata.
    
    Args:
        title: Task title/summary
        priority: P0 (critical), P1 (high), P2 (medium), P3 (low)
        billable: Whether this task is billable to a client
        client: Client name (required if billable=True)
        description: Detailed description
        pillar: Strategic pillar alignment
        estimated_hours: Estimated hours to complete
    
    Returns:
        dict with task_id, status, and task details
    """
    # Validate priority
    if priority not in ("P0", "P1", "P2", "P3"):
        return {"error": f"Invalid priority '{priority}'. Use P0, P1, P2, or P3."}
    
    # Validate billable tasks require a client
    if billable and not client:
        return {"error": "Billable tasks require a client name."}
    
    tasks = _load_tasks()
    
    # Check for duplicates
    if _is_duplicate(tasks, title, client):
        return {"error": f"Duplicate task: '{title}' for client '{client}' already exists."}
    
    # Enforce P0 limit
    if priority == "P0" and _count_p0_tasks(tasks) >= MAX_P0_TASKS:
        return {
            "error": f"Cannot create P0 task. Maximum {MAX_P0_TASKS} active P0 tasks allowed.",
            "current_p0_tasks": [
                {"id": tid, "title": t["title"]}
                for tid, t in tasks.items()
                if t.get("priority") == "P0" and t.get("status") != "completed"
            ]
        }
    
    task_id = _generate_task_id()
    tag = "[BILLABLE]" if billable else "[INTERNAL]"
    
    task = {
        "title": title,
        "description": description,
        "priority": priority,
        "tag": tag,
        "billable": billable,
        "client": client,
        "pillar": pillar,
        "status": "active",
        "estimated_hours": estimated_hours,
        "logged_hours": 0.0,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "completed_at": None
    }
    
    tasks[task_id] = task
    _save_tasks(tasks)
    
    return {
        "task_id": task_id,
        "status": "created",
        "task": task,
        "message": f"{tag} Task '{title}' created as {task_id} with priority {priority}"
    }


def list_tasks(
    status: Optional[str] = None,
    client: Optional[str] = None,
    priority: Optional[str] = None,
    billable: Optional[bool] = None
) -> dict:
    """
    List tasks with optional filters.
    
    Args:
        status: Filter by status (active, completed, blocked)
        client: Filter by client name
        priority: Filter by priority (P0, P1, P2, P3)
        billable: Filter by billable status
    
    Returns:
        dict with filtered task list and summary counts
    """
    tasks = _load_tasks()
    
    filtered = {}
    for tid, task in tasks.items():
        if status and task.get("status") != status:
            continue
        if client and task.get("client") != client:
            continue
        if priority and task.get("priority") != priority:
            continue
        if billable is not None and task.get("billable") != billable:
            continue
        filtered[tid] = task
    
    summary = {
        "total": len(filtered),
        "by_priority": {},
        "by_client": {},
        "by_status": {},
        "total_estimated_hours": 0.0,
        "total_logged_hours": 0.0
    }
    
    for task in filtered.values():
        p = task.get("priority", "unknown")
        c = task.get("client", "internal")
        s = task.get("status", "unknown")
        
        summary["by_priority"][p] = summary["by_priority"].get(p, 0) + 1
        summary["by_client"][c] = summary["by_client"].get(c, 0) + 1
        summary["by_status"][s] = summary["by_status"].get(s, 0) + 1
        summary["total_estimated_hours"] += task.get("estimated_hours", 0.0)
        summary["total_logged_hours"] += task.get("logged_hours", 0.0)
    
    return {
        "tasks": filtered,
        "summary": summary
    }


def complete_task(task_id: str, notes: str = "") -> dict:
    """Mark a task as completed."""
    
    Args:
        task_id: The unique task identifier
        notes: Completion notes
    
    Returns:
        dict with updated task details
    """
    tasks = _load_tasks()
    
    if task_id not in tasks:
        return {"error": f"Task '{task_id}' not found."}
    
    task = tasks[task_id]
    
    if task["status"] == "completed":
        return {"error": f"Task '{task_id}' is already completed."}
    
    task["status"] = "completed"
    task["completed_at"] = datetime.now().isoformat()
    task["updated_at"] = datetime.now().isoformat()
    task["completion_notes"] = notes
    
    tasks[task_id] = task
    _save_tasks(tasks)
    
    result = {
        "task_id": task_id,
        "status": "completed",
        "task": task,
        "message": f"Task '{task['title']}' marked as completed."
    }
    
    if task.get("billable"):
        result["billable_summary"] = {
            "client": task.get("client"),
            "hours_logged": task.get("logged_hours", 0.0),
            "ready_for_invoice": True
        }
    
    return result


def log_hours(
    task_id: str,
    hours: float,
    description: str = "",
    work_date: Optional[str] = None
) -> dict:
    """Log hours worked on a task."""
    
    Args:
        task_id: The unique task identifier
        hours: Number of hours to log (supports decimals, e.g. 1.5)
        description: What was accomplished
        work_date: Date of work (YYYY-MM-DD), defaults to today
    
    Returns:
        dict with updated hour totals
    """
    tasks = _load_tasks()
    
    if task_id not in tasks:
        return {"error": f"Task '{task_id}' not found."}
    
    if hours <= 0:
        return {"error": "Hours must be a positive number."}
    
    task = tasks[task_id]
    
    if work_date is None:
        work_date = date.today().isoformat()
    
    # Update task hours
    task["logged_hours"] = task.get("logged_hours", 0.0) + hours
    task["updated_at"] = datetime.now().isoformat()
    tasks[task_id] = task
    _save_tasks(tasks)
    
    # Save detailed hour entry
    all_hours = _load_hours()
    if "entries" not in all_hours:
        all_hours["entries"] = []
    
    entry = {
        "task_id": task_id,
        "hours": hours,
        "description": description,
        "work_date": work_date,
        "client": task.get("client"),
        "billable": task.get("billable", False),
        "logged_at": datetime.now().isoformat()
    }
    
    all_hours["entries"].append(entry)
    _save_hours(all_hours)
    
    return {
        "task_id": task_id,
        "hours_logged": hours,
        "total_hours_on_task": task["logged_hours"],
        "estimated_hours": task.get("estimated_hours", 0.0),
        "remaining": max(0, task.get("estimated_hours", 0.0) - task["logged_hours"]),
        "client": task.get("client"),
        "billable": task.get("billable"),
        "message": f"Logged {hours}h on '{task['title']}' (total: {task['logged_hours']}h)"
    }


def get_billable_summary(
    client: Optional[str] = None,
    period: str = "current_month"
) -> dict:
    """Get a summary of billable hours, optionally filtered by client and period."""
    
    Args:
        client: Filter by client name (None = all clients)
        period: 'current_month', 'last_month', 'current_quarter', 'all'
    
    Returns:
        dict with billable hours breakdown by client
    """
    all_hours = _load_hours()
    entries = all_hours.get("entries", [])
    
    today = date.today()
    
    # Filter by period
    filtered = []
    for entry in entries:
        if not entry.get("billable"):
            continue
        
        try:
            entry_date = date.fromisoformat(entry.get("work_date", ""))
        except (ValueError, TypeError):
            continue
        
        if period == "current_month":
            if entry_date.year == today.year and entry_date.month == today.month:
                filtered.append(entry)
        elif period == "last_month":
            last_month = today.month - 1 if today.month > 1 else 12
            last_month_year = today.year if today.month > 1 else today.year - 1
            if entry_date.year == last_month_year and entry_date.month == last_month:
                filtered.append(entry)
        elif period == "current_quarter":
            current_q = (today.month - 1) // 3
            entry_q = (entry_date.month - 1) // 3
            if entry_date.year == today.year and entry_q == current_q:
                filtered.append(entry)
        else:  # all
            filtered.append(entry)
    
    # Filter by client
    if client:
        filtered = [e for e in filtered if e.get("client") == client]
    
    # Aggregate by client
    by_client = {}
    total_hours = 0.0
    
    for entry in filtered:
        c = entry.get("client", "unknown")
        if c not in by_client:
            by_client[c] = {
                "hours": 0.0,
                "entries": 0,
                "tasks": set()
            }
        by_client[c]["hours"] += entry.get("hours", 0)
        by_client[c]["entries"] += 1
        by_client[c]["tasks"].add(entry.get("task_id", ""))
        total_hours += entry.get("hours", 0)
    
    # Convert sets to lists for serialization
    for c in by_client:
        by_client[c]["tasks"] = list(by_client[c]["tasks"])
        by_client[c]["unique_tasks"] = len(by_client[c]["tasks"])
    
    return {
        "period": period,
        "total_billable_hours": total_hours,
        "by_client": by_client,
        "entry_count": len(filtered),
        "generated_at": datetime.now().isoformat()
    }


def update_task(
    task_id: str,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    description: Optional[str] = None,
    pillar: Optional[str] = None
) -> dict:
    """Update task fields."""
    
    Args:
        task_id: The unique task identifier
        priority: New priority (P0-P3)
        status: New status (active, blocked, completed)
        description: Updated description
        pillar: Updated pillar alignment
    
    Returns:
        dict with updated task
    """
    tasks = _load_tasks()
    
    if task_id not in tasks:
        return {"error": f"Task '{task_id}' not found."}
    
    task = tasks[task_id]
    
    if priority:
        if priority not in ("P0", "P1", "P2", "P3"):
            return {"error": f"Invalid priority '{priority}'."}
        if priority == "P0" and task.get("priority") != "P0":
            if _count_p0_tasks(tasks) >= MAX_P0_TASKS:
                return {"error": f"Cannot promote to P0. Max {MAX_P0_TASKS} P0 tasks active."}
        task["priority"] = priority
    
    if status:
        if status not in ("active", "blocked", "completed"):
            return {"error": f"Invalid status '{status}'."}
        task["status"] = status
        if status == "completed":
            task["completed_at"] = datetime.now().isoformat()
    
    if description is not None:
        task["description"] = description
    
    if pillar is not None:
        task["pillar"] = pillar
    
    task["updated_at"] = datetime.now().isoformat()
    tasks[task_id] = task
    _save_tasks(tasks)
    
    return {
        "task_id": task_id,
        "status": "updated",
        "task": task,
        "message": f"Task '{task_id}' updated successfully."
    }


# ---------- Server Entry Point ----------

def get_server_info() -> dict:
    """Return server metadata and available tools."""
    return {
        "name": "work-server",
        "version": "0.1.0",
        "description": "Task management MCP server with billable tracking",
        "tools": [
            "create_task",
            "list_tasks", 
            "complete_task",
            "log_hours",
            "get_billable_summary",
            "update_task"
        ]
    }


if __name__ == "__main__":
    print("Work Server - Task Management MCP Server")
    print(f"Vault path: {VAULT_PATH}")
    print(f"Tasks file: {TASKS_FILE}")
    info = get_server_info()
    print(f"Available tools: {', '.join(info['tools'])}")
