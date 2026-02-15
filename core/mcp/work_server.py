"""
Work Server - MCP Server for Task Management

Full async implementation for managing tasks with:
- Task IDs: task-YYYYMMDD-XXX
- Tags: [BILLABLE] or [INTERNAL]
- Priority enforcement (max 3 P0s)
- Billable hours tracking per client
- YAML-based task storage
"""

import asyncio
import os
from datetime import datetime, date
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
TASKS_PATH = Path(VAULT_PATH) / "03-Tasks"


class WorkServer:
    """Async MCP Server for task and work management"""
    
    def __init__(self):
        self.server = Server("work-server")
        self.tasks_cache = {}
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup all tool handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="create_task",
                    description="Create a new task with priority, tags, and client info",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Task title"},
                            "description": {"type": "string", "description": "Task description"},
                            "priority": {
                                "type": "string",
                                "enum": ["P0", "P1", "P2", "P3"],
                                "description": "Task priority (max 3 P0s allowed)"
                            },
                            "client": {"type": "string", "description": "Client name (for billable tasks)"},
                            "is_billable": {"type": "boolean", "description": "Whether task is billable"},
                            "estimated_hours": {"type": "number", "description": "Estimated hours to complete"}
                        },
                        "required": ["title", "priority"]
                    }
                ),
                Tool(
                    name="list_tasks",
                    description="List tasks with optional filters",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["todo", "in-progress", "completed", "all"],
                                "description": "Filter by status"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["P0", "P1", "P2", "P3"],
                                "description": "Filter by priority"
                            },
                            "client": {"type": "string", "description": "Filter by client"},
                            "billable_only": {"type": "boolean", "description": "Show only billable tasks"}
                        }
                    }
                ),
                Tool(
                    name="complete_task",
                    description="Mark a task as completed",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "Task ID to complete"}
                        },
                        "required": ["task_id"]
                    }
                ),
                Tool(
                    name="log_hours",
                    description="Log hours worked on a task",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "Task ID"},
                            "hours": {"type": "number", "description": "Hours worked"},
                            "notes": {"type": "string", "description": "Work notes"}
                        },
                        "required": ["task_id", "hours"]
                    }
                ),
                Tool(
                    name="get_billable_summary",
                    description="Get billable hours summary by client",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "client": {"type": "string", "description": "Client name (optional)"},
                            "start_date": {"type": "string", "description": "Start date YYYY-MM-DD"},
                            "end_date": {"type": "string", "description": "End date YYYY-MM-DD"}
                        }
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Route tool calls to appropriate handlers"""
            
            if name == "create_task":
                result = await self._create_task(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "list_tasks":
                result = await self._list_tasks(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "complete_task":
                result = await self._complete_task(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "log_hours":
                result = await self._log_hours(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "get_billable_summary":
                result = await self._get_billable_summary(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def _create_task(
        self,
        title: str,
        priority: str,
        description: str = "",
        client: str = None,
        is_billable: bool = False,
        estimated_hours: float = 0
    ) -> Dict[str, Any]:
        """Create a new task"""
        
        # Check P0 limit
        if priority == "P0":
            p0_count = await self._count_p0_tasks()
            if p0_count >= 3:
                return {
                    "success": False,
                    "error": "Maximum 3 P0 tasks allowed. Complete or downgrade existing P0s first."
                }
        
        # Generate task ID
        today = date.today().strftime("%Y%m%d")
        task_number = await self._get_next_task_number(today)
        task_id = f"task-{today}-{task_number:03d}"
        
        # Create task data
        task = {
            "task_id": task_id,
            "title": title,
            "description": description,
            "priority": priority,
            "status": "todo",
            "tags": [],
            "client": client,
            "is_billable": is_billable,
            "estimated_hours": estimated_hours,
            "actual_hours": 0,
            "hours_log": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        # Add tags
        if is_billable:
            task["tags"].append("[BILLABLE]")
        else:
            task["tags"].append("[INTERNAL]")
        
        # Save to YAML
        await self._save_task(task)
        
        return {
            "success": True,
            "task_id": task_id,
            "message": f"Task {task_id} created successfully"
        }
    
    async def _list_tasks(
        self,
        status: str = "all",
        priority: str = None,
        client: str = None,
        billable_only: bool = False
    ) -> Dict[str, Any]:
        """List tasks with filters"""
        
        tasks = await self._load_all_tasks()
        filtered_tasks = []
        
        for task in tasks:
            # Apply filters
            if status != "all" and task.get("status") != status:
                continue
            if priority and task.get("priority") != priority:
                continue
            if client and task.get("client") != client:
                continue
            if billable_only and not task.get("is_billable"):
                continue
            
            filtered_tasks.append(task)
        
        # Sort by priority and created date
        priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        filtered_tasks.sort(
            key=lambda t: (
                priority_order.get(t.get("priority", "P3"), 3),
                t.get("created_at", "")
            )
        )
        
        return {
            "success": True,
            "count": len(filtered_tasks),
            "tasks": filtered_tasks
        }
    
    async def _complete_task(self, task_id: str) -> Dict[str, Any]:
        """Mark task as completed"""
        
        task = await self._load_task(task_id)
        if not task:
            return {"success": False, "error": f"Task {task_id} not found"}
        
        task["status"] = "completed"
        task["completed_at"] = datetime.now().isoformat()
        task["updated_at"] = datetime.now().isoformat()
        
        await self._save_task(task)
        
        return {
            "success": True,
            "message": f"Task {task_id} marked as completed",
            "billable_hours": task.get("actual_hours", 0) if task.get("is_billable") else 0
        }
    
    async def _log_hours(
        self,
        task_id: str,
        hours: float,
        notes: str = ""
    ) -> Dict[str, Any]:
        """Log hours worked on a task"""
        
        task = await self._load_task(task_id)
        if not task:
            return {"success": False, "error": f"Task {task_id} not found"}
        
        # Add hours log entry
        log_entry = {
            "date": datetime.now().isoformat(),
            "hours": hours,
            "notes": notes
        }
        
        if "hours_log" not in task:
            task["hours_log"] = []
        task["hours_log"].append(log_entry)
        
        # Update actual hours
        task["actual_hours"] = task.get("actual_hours", 0) + hours
        task["updated_at"] = datetime.now().isoformat()
        
        await self._save_task(task)
        
        return {
            "success": True,
            "message": f"Logged {hours} hours to {task_id}",
            "total_hours": task["actual_hours"]
        }
    
    async def _get_billable_summary(
        self,
        client: str = None,
        start_date: str = None,
        end_date: str = None
    ) -> Dict[str, Any]:
        """Get billable hours summary"""
        
        tasks = await self._load_all_tasks()
        
        # Parse dates
        start = datetime.fromisoformat(start_date) if start_date else None
        end = datetime.fromisoformat(end_date) if end_date else None
        
        summary = {}
        total_hours = 0
        
        for task in tasks:
            if not task.get("is_billable"):
                continue
            
            task_client = task.get("client", "Unknown")
            
            # Apply filters
            if client and task_client != client:
                continue
            
            # Check date range for hours log
            task_hours = 0
            for log in task.get("hours_log", []):
                log_date = datetime.fromisoformat(log["date"])
                if start and log_date < start:
                    continue
                if end and log_date > end:
                    continue
                task_hours += log["hours"]
            
            if task_hours > 0:
                if task_client not in summary:
                    summary[task_client] = {
                        "hours": 0,
                        "tasks": []
                    }
                summary[task_client]["hours"] += task_hours
                summary[task_client]["tasks"].append({
                    "task_id": task["task_id"],
                    "title": task["title"],
                    "hours": task_hours
                })
                total_hours += task_hours
        
        return {
            "success": True,
            "total_hours": total_hours,
            "by_client": summary
        }
    
    async def _count_p0_tasks(self) -> int:
        """Count active P0 tasks"""
        tasks = await self._load_all_tasks()
        return sum(
            1 for task in tasks
            if task.get("priority") == "P0" and task.get("status") != "completed"
        )
    
    async def _get_next_task_number(self, date_str: str) -> int:
        """Get next task number for the day"""
        tasks = await self._load_all_tasks()
        matching = [
            t for t in tasks
            if t.get("task_id", "").startswith(f"task-{date_str}-")
        ]
        return len(matching) + 1
    
    async def _save_task(self, task: Dict[str, Any]):
        """Save task to YAML file"""
        TASKS_PATH.mkdir(parents=True, exist_ok=True)
        
        task_file = TASKS_PATH / f"{task['task_id']}.yaml"
        with open(task_file, 'w') as f:
            yaml.safe_dump(task, f, default_flow_style=False, sort_keys=False)
        
        self.tasks_cache[task['task_id']] = task
    
    async def _load_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Load task from YAML file"""
        if task_id in self.tasks_cache:
            return self.tasks_cache[task_id]
        
        task_file = TASKS_PATH / f"{task_id}.yaml"
        if not task_file.exists():
            return None
        
        with open(task_file, 'r') as f:
            task = yaml.safe_load(f)
        
        self.tasks_cache[task_id] = task
        return task
    
    async def _load_all_tasks(self) -> List[Dict[str, Any]]:
        """Load all tasks from YAML files"""
        if not TASKS_PATH.exists():
            return []
        
        tasks = []
        for task_file in TASKS_PATH.glob("task-*.yaml"):
            with open(task_file, 'r') as f:
                task = yaml.safe_load(f)
                if task:
                    tasks.append(task)
        
        return tasks


async def main():
    """Run the work server"""
    work_server = WorkServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await work_server.server.run(
            read_stream,
            write_stream,
            work_server.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
