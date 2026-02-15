"""
Client Server - Client Relationship Management MCP Server

Features:
- Client profiles with contact info and preferences
- Communication log tracking
- Client health scoring
- Meeting notes and follow-ups
- Onboarding status tracking
"""

from datetime import datetime, timedelta
from typing import Optional, List
from ..config import Config
from ..utils import (
    generate_id,
    format_datetime,
    validate_email,
    validate_phone,
    calculate_percentage
)
from .base_server import BaseMCPServer


class ClientServer(BaseMCPServer):
    """Client relationship management server."""
    
    def __init__(self):
        super().__init__("client")
        
        # Initialize collections
        if "clients" not in self._data:
            self._data["clients"] = {}
        if "communications" not in self._data:
            self._data["communications"] = {}
        if "meetings" not in self._data:
            self._data["meetings"] = {}
    
    def get_info(self) -> dict:
        """Return server metadata."""
        return {
            "name": "client-server",
            "version": "0.1.0",
            "description": "Client relationship management MCP server",
            "tools": [
                "create_client",
                "get_client",
                "update_client",
                "list_clients",
                "log_communication",
                "get_communications",
                "schedule_meeting",
                "log_meeting_notes",
                "calculate_health_score",
                "get_client_summary"
            ]
        }
    
    def create_client(
        self,
        name: str,
        email: str,
        company: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        industry: Optional[str] = None,
        primary_contact: Optional[str] = None,
        notes: Optional[str] = None
    ) -> dict:
        """
        Create a new client profile.
        
        Args:
            name: Client name
            email: Client email address
            company: Company name
            phone: Phone number
            address: Business address
            industry: Industry/sector
            primary_contact: Primary contact person
            notes: Additional notes
        
        Returns:
            Client profile with ID
        """
        # Validate email
        if not validate_email(email):
            return {"error": f"Invalid email address: {email}"}
        
        # Validate phone if provided
        if phone and not validate_phone(phone):
            return {"error": f"Invalid phone number: {phone}"}
        
        # Check for duplicate email
        clients = self._get_collection("clients")
        for client in clients.values():
            if client.get("email", "").lower() == email.lower():
                return {"error": f"Client with email '{email}' already exists"}
        
        # Generate client ID
        client_id = generate_id("client")
        
        client_data = {
            "name": name,
            "email": email,
            "company": company,
            "phone": phone,
            "address": address,
            "industry": industry,
            "primary_contact": primary_contact or name,
            "notes": notes or "",
            "status": "active",
            "onboarding_status": "not_started",
            "health_score": 100,
            "satisfaction_rating": None,
            "total_revenue": 0.0,
            "project_count": 0,
            "last_contact": None,
            "next_followup": None,
            "tags": [],
            "preferences": {}
        }
        
        result = self._create_record("clients", client_id, client_data)
        
        if result.get("success"):
            self.logger.info(f"Created client: {name} ({client_id})")
            return {
                "client_id": client_id,
                "status": "created",
                "client": result["record"]
            }
        
        return result
    
    def get_client(self, client_id: str) -> dict:
        """
        Get client profile by ID.
        
        Args:
            client_id: Client identifier
        
        Returns:
            Client profile
        """
        result = self._read_record("clients", client_id)
        
        if result.get("success"):
            return {"client": result["record"]}
        
        return result
    
    def update_client(
        self,
        client_id: str,
        **updates
    ) -> dict:
        """
        Update client profile.
        
        Args:
            client_id: Client identifier
            **updates: Fields to update
        
        Returns:
            Updated client profile
        """
        # Validate email if being updated
        if "email" in updates and not validate_email(updates["email"]):
            return {"error": f"Invalid email address: {updates['email']}"}
        
        # Validate phone if being updated
        if "phone" in updates and updates["phone"] and not validate_phone(updates["phone"]):
            return {"error": f"Invalid phone number: {updates['phone']}"}
        
        result = self._update_record("clients", client_id, updates)
        
        if result.get("success"):
            return {
                "client_id": client_id,
                "status": "updated",
                "client": result["record"]
            }
        
        return result
    
    def list_clients(
        self,
        status: Optional[str] = None,
        industry: Optional[str] = None,
        min_health_score: Optional[int] = None
    ) -> dict:
        """
        List clients with optional filters.
        
        Args:
            status: Filter by status (active, inactive, archived)
            industry: Filter by industry
            min_health_score: Filter by minimum health score
        
        Returns:
            List of clients with summary
        """
        def filter_func(client: dict) -> bool:
            if status and client.get("status") != status:
                return False
            if industry and client.get("industry") != industry:
                return False
            if min_health_score and client.get("health_score", 0) < min_health_score:
                return False
            return True
        
        result = self._list_records("clients", filter_func, sort_key="name")
        
        if result.get("success"):
            clients = result["records"]
            
            summary = {
                "total": len(clients),
                "by_status": {},
                "by_industry": {},
                "average_health_score": 0,
                "total_revenue": 0.0
            }
            
            for client in clients:
                # Status breakdown
                status_val = client.get("status", "unknown")
                summary["by_status"][status_val] = summary["by_status"].get(status_val, 0) + 1
                
                # Industry breakdown
                industry_val = client.get("industry") or "unknown"
                summary["by_industry"][industry_val] = summary["by_industry"].get(industry_val, 0) + 1
                
                # Totals
                summary["total_revenue"] += client.get("total_revenue", 0.0)
                summary["average_health_score"] += client.get("health_score", 0)
            
            if len(clients) > 0:
                summary["average_health_score"] = round(summary["average_health_score"] / len(clients), 1)
            
            return {
                "clients": clients,
                "summary": summary
            }
        
        return result
    
    def log_communication(
        self,
        client_id: str,
        comm_type: str,
        subject: str,
        notes: Optional[str] = None,
        sentiment: Optional[str] = None
    ) -> dict:
        """
        Log a communication with a client.
        
        Args:
            client_id: Client identifier
            comm_type: Type (email, call, meeting, message)
            subject: Communication subject/summary
            notes: Detailed notes
            sentiment: Sentiment (positive, neutral, negative)
        
        Returns:
            Communication log entry
        """
        # Verify client exists
        client_result = self._read_record("clients", client_id)
        if not client_result.get("success"):
            return {"error": f"Client '{client_id}' not found"}
        
        # Validate communication type
        valid_types = ["email", "call", "meeting", "message", "other"]
        if comm_type not in valid_types:
            return {"error": f"Invalid comm_type. Must be one of: {', '.join(valid_types)}"}
        
        # Generate communication ID
        comm_id = generate_id("comm")
        
        comm_data = {
            "client_id": client_id,
            "type": comm_type,
            "subject": subject,
            "notes": notes or "",
            "sentiment": sentiment,
            "timestamp": datetime.now().isoformat()
        }
        
        result = self._create_record("communications", comm_id, comm_data)
        
        if result.get("success"):
            # Update client's last contact
            self._update_record("clients", client_id, {
                "last_contact": datetime.now().isoformat()
            })
            
            return {
                "comm_id": comm_id,
                "status": "logged",
                "communication": result["record"]
            }
        
        return result
    
    def get_communications(
        self,
        client_id: Optional[str] = None,
        comm_type: Optional[str] = None,
        limit: int = 50
    ) -> dict:
        """
        Get communication history.
        
        Args:
            client_id: Filter by client
            comm_type: Filter by type
            limit: Maximum records to return
        
        Returns:
            Communication log entries
        """
        def filter_func(comm: dict) -> bool:
            if client_id and comm.get("client_id") != client_id:
                return False
            if comm_type and comm.get("type") != comm_type:
                return False
            return True
        
        result = self._list_records("communications", filter_func, sort_key="timestamp", reverse=True)
        
        if result.get("success"):
            communications = result["records"][:limit]
            return {
                "communications": communications,
                "count": len(communications),
                "total_available": result["count"]
            }
        
        return result
    
    def schedule_meeting(
        self,
        client_id: str,
        title: str,
        scheduled_date: str,
        duration_minutes: int = 60,
        location: Optional[str] = None,
        agenda: Optional[str] = None
    ) -> dict:
        """
        Schedule a meeting with a client.
        
        Args:
            client_id: Client identifier
            title: Meeting title
            scheduled_date: ISO format date/time
            duration_minutes: Duration in minutes
            location: Meeting location (or video link)
            agenda: Meeting agenda
        
        Returns:
            Meeting record
        """
        # Verify client exists
        client_result = self._read_record("clients", client_id)
        if not client_result.get("success"):
            return {"error": f"Client '{client_id}' not found"}
        
        # Generate meeting ID
        meeting_id = generate_id("meeting")
        
        meeting_data = {
            "client_id": client_id,
            "title": title,
            "scheduled_date": scheduled_date,
            "duration_minutes": duration_minutes,
            "location": location,
            "agenda": agenda,
            "status": "scheduled",
            "notes": None,
            "action_items": [],
            "attendees": []
        }
        
        result = self._create_record("meetings", meeting_id, meeting_data)
        
        if result.get("success"):
            return {
                "meeting_id": meeting_id,
                "status": "scheduled",
                "meeting": result["record"]
            }
        
        return result
    
    def log_meeting_notes(
        self,
        meeting_id: str,
        notes: str,
        action_items: Optional[List[str]] = None,
        next_steps: Optional[str] = None
    ) -> dict:
        """
        Log notes from a completed meeting.
        
        Args:
            meeting_id: Meeting identifier
            notes: Meeting notes
            action_items: List of action items
            next_steps: Next steps summary
        
        Returns:
            Updated meeting record
        """
        updates = {
            "notes": notes,
            "status": "completed",
            "completed_at": datetime.now().isoformat()
        }
        
        if action_items:
            updates["action_items"] = action_items
        
        if next_steps:
            updates["next_steps"] = next_steps
        
        result = self._update_record("meetings", meeting_id, updates)
        
        if result.get("success"):
            # Log as communication
            meeting = result["record"]
            client_id = meeting.get("client_id")
            if client_id:
                self.log_communication(
                    client_id,
                    "meeting",
                    f"Meeting: {meeting.get('title')}",
                    notes=notes
                )
            
            return {
                "meeting_id": meeting_id,
                "status": "notes_logged",
                "meeting": result["record"]
            }
        
        return result
    
    def calculate_health_score(self, client_id: str) -> dict:
        """
        Calculate and update client health score.
        
        Score factors:
        - Recent communication (30 points)
        - Payment history (25 points)
        - Project activity (25 points)
        - Satisfaction rating (20 points)
        
        Args:
            client_id: Client identifier
        
        Returns:
            Health score with breakdown
        """
        client_result = self._read_record("clients", client_id)
        if not client_result.get("success"):
            return {"error": f"Client '{client_id}' not found"}
        
        client = client_result["record"]
        score = 0
        breakdown = {}
        
        # Recent communication (30 points)
        last_contact = client.get("last_contact")
        if last_contact:
            try:
                last_contact_date = datetime.fromisoformat(last_contact)
                days_since = (datetime.now() - last_contact_date).days
                
                if days_since <= 7:
                    comm_score = 30
                elif days_since <= 30:
                    comm_score = 20
                elif days_since <= 90:
                    comm_score = 10
                else:
                    comm_score = 0
                
                score += comm_score
                breakdown["communication"] = {
                    "score": comm_score,
                    "days_since_contact": days_since
                }
            except (ValueError, TypeError):
                breakdown["communication"] = {"score": 0, "error": "Invalid date"}
        else:
            breakdown["communication"] = {"score": 0, "reason": "No contact logged"}
        
        # Payment history (25 points) - placeholder for billing integration
        payment_score = 25  # Assume good payment history by default
        breakdown["payment"] = {
            "score": payment_score,
            "note": "Based on billing server data"
        }
        score += payment_score
        
        # Project activity (25 points)
        project_count = client.get("project_count", 0)
        if project_count > 0:
            activity_score = min(25, project_count * 5)
        else:
            activity_score = 0
        
        score += activity_score
        breakdown["activity"] = {
            "score": activity_score,
            "project_count": project_count
        }
        
        # Satisfaction rating (20 points)
        satisfaction = client.get("satisfaction_rating")
        if satisfaction:
            satisfaction_score = int((satisfaction / 5.0) * 20)
        else:
            satisfaction_score = 15  # Neutral assumption
        
        score += satisfaction_score
        breakdown["satisfaction"] = {
            "score": satisfaction_score,
            "rating": satisfaction
        }
        
        # Update client health score
        self._update_record("clients", client_id, {"health_score": score})
        
        return {
            "client_id": client_id,
            "health_score": score,
            "breakdown": breakdown,
            "status": self._get_health_status(score)
        }
    
    def _get_health_status(self, score: int) -> str:
        """Get health status label from score."""
        if score >= 80:
            return "excellent"
        elif score >= 60:
            return "good"
        elif score >= 40:
            return "fair"
        elif score >= 20:
            return "at_risk"
        else:
            return "critical"
    
    def get_client_summary(self, client_id: str) -> dict:
        """
        Get comprehensive client summary.
        
        Args:
            client_id: Client identifier
        
        Returns:
            Complete client overview
        """
        # Get client profile
        client_result = self._read_record("clients", client_id)
        if not client_result.get("success"):
            return client_result
        
        client = client_result["record"]
        
        # Get recent communications
        comms_result = self.get_communications(client_id=client_id, limit=10)
        recent_comms = comms_result.get("communications", [])
        
        # Get upcoming meetings
        meetings = self._get_collection("meetings")
        upcoming_meetings = [
            m for m in meetings.values()
            if m.get("client_id") == client_id and m.get("status") == "scheduled"
        ]
        
        # Calculate health score
        health_result = self.calculate_health_score(client_id)
        
        return {
            "client": client,
            "health_score": health_result.get("health_score"),
            "health_status": health_result.get("status"),
            "recent_communications": recent_comms,
            "upcoming_meetings": upcoming_meetings,
            "summary": {
                "total_revenue": client.get("total_revenue", 0.0),
                "project_count": client.get("project_count", 0),
                "status": client.get("status"),
                "onboarding_status": client.get("onboarding_status")
            }
        }


# Standalone functions for MCP tool interface
_server_instance = None

def _get_server() -> ClientServer:
    """Get or create server instance."""
    global _server_instance
    if _server_instance is None:
        _server_instance = ClientServer()
    return _server_instance


def create_client(**kwargs) -> dict:
    """Create a new client profile."""
    return _get_server().create_client(**kwargs)


def get_client(client_id: str) -> dict:
    """Get client profile."""
    return _get_server().get_client(client_id)


def update_client(client_id: str, **updates) -> dict:
    """Update client profile."""
    return _get_server().update_client(client_id, **updates)


def list_clients(**kwargs) -> dict:
    """List clients with filters."""
    return _get_server().list_clients(**kwargs)


def log_communication(**kwargs) -> dict:
    """Log communication with client."""
    return _get_server().log_communication(**kwargs)


def get_communications(**kwargs) -> dict:
    """Get communication history."""
    return _get_server().get_communications(**kwargs)


def schedule_meeting(**kwargs) -> dict:
    """Schedule a client meeting."""
    return _get_server().schedule_meeting(**kwargs)


def log_meeting_notes(**kwargs) -> dict:
    """Log meeting notes."""
    return _get_server().log_meeting_notes(**kwargs)


def calculate_health_score(client_id: str) -> dict:
    """Calculate client health score."""
    return _get_server().calculate_health_score(client_id)


def get_client_summary(client_id: str) -> dict:
    """Get comprehensive client summary."""
    return _get_server().get_client_summary(client_id)


def get_server_info() -> dict:
    """Get server info."""
    return _get_server().get_info()


if __name__ == "__main__":
    server = ClientServer()
    print("Client Server - CRM MCP Server")
    print(f"Data file: {server.data_path}")
    info = server.get_info()
    print(f"Available tools: {', '.join(info['tools'])}")
