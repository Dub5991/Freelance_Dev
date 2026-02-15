"""
Career Server - Career Development and Skills Tracking MCP Server

Features:
- Skills inventory and gap analysis
- Learning goals and progress tracking
- Portfolio project management
- Rate history and market rate comparison
- Professional network tracking
- Career milestone tracking
"""

from datetime import datetime, date
from typing import Optional, List, Dict
from ..config import Config
from ..utils import generate_id, format_date, format_currency
from .base_server import BaseMCPServer


class CareerServer(BaseMCPServer):
    """Career development and professional growth tracking server."""
    
    def __init__(self):
        super().__init__("career")
        
        # Initialize collections
        if "skills" not in self._data:
            self._data["skills"] = {}
        
        if "learning_goals" not in self._data:
            self._data["learning_goals"] = {}
        
        if "portfolio_projects" not in self._data:
            self._data["portfolio_projects"] = {}
        
        if "rate_history" not in self._data:
            self._data["rate_history"] = {}
        
        if "network_contacts" not in self._data:
            self._data["network_contacts"] = {}
        
        if "milestones" not in self._data:
            self._data["milestones"] = {}
    
    def get_info(self) -> dict:
        """Return server metadata."""
        return {
            "name": "career-server",
            "version": "0.1.0",
            "description": "Career development and skills tracking MCP server",
            "tools": [
                "add_skill",
                "update_skill_level",
                "get_skills_inventory",
                "identify_skill_gaps",
                "create_learning_goal",
                "update_learning_progress",
                "list_learning_goals",
                "add_portfolio_project",
                "get_portfolio",
                "record_rate_change",
                "get_rate_history",
                "add_network_contact",
                "list_network_contacts",
                "add_milestone",
                "get_career_summary"
            ]
        }
    
    def add_skill(
        self,
        skill_name: str,
        category: str,
        proficiency_level: int,
        years_experience: float = 0.0,
        last_used: Optional[str] = None,
        notes: Optional[str] = None
    ) -> dict:
        """
        Add a skill to inventory.
        
        Args:
            skill_name: Name of the skill
            category: Category (programming, framework, tool, soft_skill, domain_knowledge, other)
            proficiency_level: Proficiency (1=beginner, 2=intermediate, 3=advanced, 4=expert, 5=master)
            years_experience: Years of experience with this skill
            last_used: Last date used (ISO format)
            notes: Additional notes
        
        Returns:
            Skill record
        """
        if not 1 <= proficiency_level <= 5:
            return {"error": "Proficiency level must be between 1 and 5"}
        
        valid_categories = [
            "programming",
            "framework",
            "tool",
            "soft_skill",
            "domain_knowledge",
            "other"
        ]
        
        if category not in valid_categories:
            return {
                "error": f"Invalid category. Must be one of: {', '.join(valid_categories)}"
            }
        
        # Check for duplicate
        skills = self._get_collection("skills")
        for skill in skills.values():
            if skill.get("name", "").lower() == skill_name.lower():
                return {"error": f"Skill '{skill_name}' already exists"}
        
        skill_id = generate_id("skill", date_part=False)
        
        skill_data = {
            "name": skill_name,
            "category": category,
            "proficiency_level": proficiency_level,
            "years_experience": years_experience,
            "last_used": last_used or date.today().isoformat(),
            "notes": notes or "",
            "endorsements": 0,
            "projects_used_in": []
        }
        
        result = self._create_record("skills", skill_id, skill_data)
        
        if result.get("success"):
            return {
                "skill_id": skill_id,
                "status": "added",
                "skill": result["record"]
            }
        
        return result
    
    def update_skill_level(
        self,
        skill_id: str,
        proficiency_level: Optional[int] = None,
        years_experience: Optional[float] = None,
        last_used: Optional[str] = None,
        notes: Optional[str] = None
    ) -> dict:
        """
        Update skill proficiency and details.
        
        Args:
            skill_id: Skill identifier
            proficiency_level: New proficiency level
            years_experience: Updated years of experience
            last_used: Last used date
            notes: Additional notes
        
        Returns:
            Updated skill
        """
        updates = {}
        
        if proficiency_level is not None:
            if not 1 <= proficiency_level <= 5:
                return {"error": "Proficiency level must be between 1 and 5"}
            updates["proficiency_level"] = proficiency_level
        
        if years_experience is not None:
            updates["years_experience"] = years_experience
        
        if last_used is not None:
            updates["last_used"] = last_used
        
        if notes is not None:
            updates["notes"] = notes
        
        result = self._update_record("skills", skill_id, updates)
        
        if result.get("success"):
            return {
                "skill_id": skill_id,
                "status": "updated",
                "skill": result["record"]
            }
        
        return result
    
    def get_skills_inventory(
        self,
        category: Optional[str] = None,
        min_proficiency: Optional[int] = None
    ) -> dict:
        """
        Get skills inventory.
        
        Args:
            category: Filter by category
            min_proficiency: Filter by minimum proficiency level
        
        Returns:
            Skills inventory with breakdown
        """
        def filter_func(skill: dict) -> bool:
            if category and skill.get("category") != category:
                return False
            if min_proficiency and skill.get("proficiency_level", 0) < min_proficiency:
                return False
            return True
        
        result = self._list_records("skills", filter_func)
        
        if result.get("success"):
            skills = result["records"]
            
            summary = {
                "total_skills": len(skills),
                "by_category": {},
                "by_proficiency": {
                    "beginner": 0,
                    "intermediate": 0,
                    "advanced": 0,
                    "expert": 0,
                    "master": 0
                },
                "average_proficiency": 0
            }
            
            proficiency_labels = ["", "beginner", "intermediate", "advanced", "expert", "master"]
            total_proficiency = 0
            
            for skill in skills:
                # Category breakdown
                cat = skill.get("category", "unknown")
                summary["by_category"][cat] = summary["by_category"].get(cat, 0) + 1
                
                # Proficiency breakdown
                prof = skill.get("proficiency_level", 1)
                total_proficiency += prof
                label = proficiency_labels[prof] if 1 <= prof <= 5 else "unknown"
                summary["by_proficiency"][label] += 1
            
            if len(skills) > 0:
                summary["average_proficiency"] = round(total_proficiency / len(skills), 2)
            
            return {
                "skills": skills,
                "summary": summary
            }
        
        return result
    
    def identify_skill_gaps(
        self,
        target_role: str,
        required_skills: List[str]
    ) -> dict:
        """
        Identify skill gaps for a target role.
        
        Args:
            target_role: Target job role or position
            required_skills: List of required skill names
        
        Returns:
            Gap analysis with recommendations
        """
        skills_result = self.get_skills_inventory()
        current_skills = skills_result.get("skills", [])
        current_skill_names = [s.get("name", "").lower() for s in current_skills]
        
        # Identify gaps
        gaps = []
        for required_skill in required_skills:
            if required_skill.lower() not in current_skill_names:
                gaps.append({
                    "skill": required_skill,
                    "status": "missing",
                    "recommendation": f"Learn {required_skill} to meet requirements"
                })
        
        # Identify skills that need improvement
        needs_improvement = []
        for skill in current_skills:
            skill_name = skill.get("name", "")
            if skill_name.lower() in [rs.lower() for rs in required_skills]:
                prof = skill.get("proficiency_level", 0)
                if prof < 3:  # Less than advanced
                    needs_improvement.append({
                        "skill": skill_name,
                        "current_level": prof,
                        "recommended_level": 3,
                        "recommendation": f"Improve {skill_name} from level {prof} to level 3 (advanced)"
                    })
        
        return {
            "target_role": target_role,
            "required_skills": required_skills,
            "gaps": gaps,
            "needs_improvement": needs_improvement,
            "gap_count": len(gaps),
            "improvement_count": len(needs_improvement)
        }
    
    def create_learning_goal(
        self,
        goal_title: str,
        skill_name: str,
        target_proficiency: int,
        timeline_days: int,
        resources: Optional[List[str]] = None,
        milestones: Optional[List[str]] = None
    ) -> dict:
        """
        Create a learning goal.
        
        Args:
            goal_title: Goal title
            skill_name: Skill to learn/improve
            target_proficiency: Target proficiency level (1-5)
            timeline_days: Days to achieve goal
            resources: Learning resources (courses, books, etc.)
            milestones: Learning milestones
        
        Returns:
            Learning goal record
        """
        if not 1 <= target_proficiency <= 5:
            return {"error": "Target proficiency must be between 1 and 5"}
        
        goal_id = generate_id("goal")
        
        target_date = (date.today() + timedelta(days=timeline_days)).isoformat()
        
        goal_data = {
            "title": goal_title,
            "skill_name": skill_name,
            "target_proficiency": target_proficiency,
            "timeline_days": timeline_days,
            "target_date": target_date,
            "resources": resources or [],
            "milestones": milestones or [],
            "status": "in_progress",
            "progress_percent": 0,
            "completed_date": None,
            "notes": ""
        }
        
        result = self._create_record("learning_goals", goal_id, goal_data)
        
        if result.get("success"):
            return {
                "goal_id": goal_id,
                "status": "created",
                "goal": result["record"]
            }
        
        return result
    
    def update_learning_progress(
        self,
        goal_id: str,
        progress_percent: int,
        notes: Optional[str] = None,
        completed: bool = False
    ) -> dict:
        """
        Update learning goal progress.
        
        Args:
            goal_id: Goal identifier
            progress_percent: Progress percentage (0-100)
            notes: Progress notes
            completed: Mark as completed
        
        Returns:
            Updated goal
        """
        if not 0 <= progress_percent <= 100:
            return {"error": "Progress must be between 0 and 100"}
        
        updates = {"progress_percent": progress_percent}
        
        if notes:
            updates["notes"] = notes
        
        if completed or progress_percent >= 100:
            updates["status"] = "completed"
            updates["completed_date"] = date.today().isoformat()
        
        result = self._update_record("learning_goals", goal_id, updates)
        
        if result.get("success"):
            return {
                "goal_id": goal_id,
                "status": "updated",
                "goal": result["record"]
            }
        
        return result
    
    def list_learning_goals(
        self,
        status: Optional[str] = None
    ) -> dict:
        """
        List learning goals.
        
        Args:
            status: Filter by status (in_progress, completed, abandoned)
        
        Returns:
            List of learning goals
        """
        def filter_func(goal: dict) -> bool:
            if status and goal.get("status") != status:
                return False
            return True
        
        result = self._list_records("learning_goals", filter_func, sort_key="target_date")
        
        if result.get("success"):
            goals = result["records"]
            
            summary = {
                "total_goals": len(goals),
                "by_status": {},
                "average_progress": 0
            }
            
            total_progress = 0
            for goal in goals:
                goal_status = goal.get("status", "unknown")
                summary["by_status"][goal_status] = summary["by_status"].get(goal_status, 0) + 1
                total_progress += goal.get("progress_percent", 0)
            
            if len(goals) > 0:
                summary["average_progress"] = round(total_progress / len(goals), 1)
            
            return {
                "goals": goals,
                "summary": summary
            }
        
        return result
    
    def add_portfolio_project(
        self,
        project_name: str,
        description: str,
        technologies: List[str],
        url: Optional[str] = None,
        github_url: Optional[str] = None,
        role: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        highlights: Optional[List[str]] = None
    ) -> dict:
        """
        Add a portfolio project.
        
        Args:
            project_name: Project name
            description: Project description
            technologies: Technologies used
            url: Live project URL
            github_url: GitHub repository URL
            role: Your role in the project
            start_date: Project start date
            end_date: Project end date
            highlights: Key achievements/highlights
        
        Returns:
            Portfolio project record
        """
        project_id = generate_id("project", date_part=False)
        
        project_data = {
            "name": project_name,
            "description": description,
            "technologies": technologies,
            "url": url,
            "github_url": github_url,
            "role": role,
            "start_date": start_date or date.today().isoformat(),
            "end_date": end_date,
            "highlights": highlights or [],
            "featured": False,
            "views": 0
        }
        
        result = self._create_record("portfolio_projects", project_id, project_data)
        
        if result.get("success"):
            # Update skills used in projects
            skills = self._get_collection("skills")
            for skill_id, skill in skills.items():
                skill_name = skill.get("name", "").lower()
                if any(tech.lower() == skill_name for tech in technologies):
                    projects_list = skill.get("projects_used_in", [])
                    if project_id not in projects_list:
                        projects_list.append(project_id)
                        self._update_record("skills", skill_id, {
                            "projects_used_in": projects_list
                        })
            
            return {
                "project_id": project_id,
                "status": "added",
                "project": result["record"]
            }
        
        return result
    
    def get_portfolio(
        self,
        featured_only: bool = False
    ) -> dict:
        """
        Get portfolio projects.
        
        Args:
            featured_only: Show only featured projects
        
        Returns:
            Portfolio projects
        """
        def filter_func(project: dict) -> bool:
            if featured_only and not project.get("featured"):
                return False
            return True
        
        result = self._list_records(
            "portfolio_projects",
            filter_func,
            sort_key="start_date",
            reverse=True
        )
        
        if result.get("success"):
            return {
                "projects": result["records"],
                "count": result["count"]
            }
        
        return result
    
    def record_rate_change(
        self,
        rate_type: str,
        amount: float,
        currency: str = "USD",
        effective_date: Optional[str] = None,
        reason: Optional[str] = None
    ) -> dict:
        """
        Record a rate change.
        
        Args:
            rate_type: Type of rate (hourly, daily, project)
            amount: Rate amount
            currency: Currency code
            effective_date: When rate becomes effective
            reason: Reason for change
        
        Returns:
            Rate record
        """
        rate_id = generate_id("rate")
        
        rate_data = {
            "type": rate_type,
            "amount": amount,
            "currency": currency,
            "effective_date": effective_date or date.today().isoformat(),
            "reason": reason or "Rate adjustment"
        }
        
        result = self._create_record("rate_history", rate_id, rate_data)
        
        if result.get("success"):
            # Update config default if hourly rate
            if rate_type == "hourly":
                Config.DEFAULT_HOURLY_RATE = amount
            
            return {
                "rate_id": rate_id,
                "status": "recorded",
                "rate": result["record"]
            }
        
        return result
    
    def get_rate_history(
        self,
        rate_type: Optional[str] = None
    ) -> dict:
        """
        Get rate history.
        
        Args:
            rate_type: Filter by rate type
        
        Returns:
            Rate history with analysis
        """
        def filter_func(rate: dict) -> bool:
            if rate_type and rate.get("type") != rate_type:
                return False
            return True
        
        result = self._list_records(
            "rate_history",
            filter_func,
            sort_key="effective_date",
            reverse=True
        )
        
        if result.get("success"):
            rates = result["records"]
            
            # Calculate growth
            if len(rates) >= 2:
                latest = rates[0].get("amount", 0)
                earliest = rates[-1].get("amount", 1)
                growth_percent = ((latest - earliest) / earliest * 100) if earliest > 0 else 0
            else:
                growth_percent = 0
            
            return {
                "rates": rates,
                "count": len(rates),
                "current_rate": rates[0] if rates else None,
                "growth_percent": round(growth_percent, 2)
            }
        
        return result
    
    def add_network_contact(
        self,
        name: str,
        relationship: str,
        company: Optional[str] = None,
        role: Optional[str] = None,
        email: Optional[str] = None,
        linkedin: Optional[str] = None,
        notes: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> dict:
        """
        Add a professional network contact.
        
        Args:
            name: Contact name
            relationship: Relationship type (client, mentor, peer, referral_source, former_colleague, other)
            company: Company name
            role: Job role/title
            email: Email address
            linkedin: LinkedIn profile URL
            notes: Notes about contact
            tags: Contact tags
        
        Returns:
            Network contact record
        """
        contact_id = generate_id("contact", date_part=False)
        
        contact_data = {
            "name": name,
            "relationship": relationship,
            "company": company,
            "role": role,
            "email": email,
            "linkedin": linkedin,
            "notes": notes or "",
            "tags": tags or [],
            "last_contact": date.today().isoformat(),
            "referrals_given": 0,
            "referrals_received": 0
        }
        
        result = self._create_record("network_contacts", contact_id, contact_data)
        
        if result.get("success"):
            return {
                "contact_id": contact_id,
                "status": "added",
                "contact": result["record"]
            }
        
        return result
    
    def list_network_contacts(
        self,
        relationship: Optional[str] = None,
        tag: Optional[str] = None
    ) -> dict:
        """
        List professional network contacts.
        
        Args:
            relationship: Filter by relationship type
            tag: Filter by tag
        
        Returns:
            Network contacts
        """
        def filter_func(contact: dict) -> bool:
            if relationship and contact.get("relationship") != relationship:
                return False
            if tag and tag not in contact.get("tags", []):
                return False
            return True
        
        result = self._list_records("network_contacts", filter_func, sort_key="name")
        
        if result.get("success"):
            contacts = result["records"]
            
            summary = {
                "total_contacts": len(contacts),
                "by_relationship": {}
            }
            
            for contact in contacts:
                rel = contact.get("relationship", "unknown")
                summary["by_relationship"][rel] = summary["by_relationship"].get(rel, 0) + 1
            
            return {
                "contacts": contacts,
                "summary": summary
            }
        
        return result
    
    def add_milestone(
        self,
        milestone_title: str,
        description: str,
        achieved_date: Optional[str] = None,
        category: str = "achievement",
        impact: Optional[str] = None
    ) -> dict:
        """
        Add a career milestone.
        
        Args:
            milestone_title: Milestone title
            description: Detailed description
            achieved_date: Date achieved
            category: Category (achievement, certification, promotion, project_completion, revenue_milestone, other)
            impact: Impact description
        
        Returns:
            Milestone record
        """
        milestone_id = generate_id("milestone", date_part=False)
        
        milestone_data = {
            "title": milestone_title,
            "description": description,
            "achieved_date": achieved_date or date.today().isoformat(),
            "category": category,
            "impact": impact or ""
        }
        
        result = self._create_record("milestones", milestone_id, milestone_data)
        
        if result.get("success"):
            return {
                "milestone_id": milestone_id,
                "status": "added",
                "milestone": result["record"]
            }
        
        return result
    
    def get_career_summary(self) -> dict:
        """
        Get comprehensive career summary.
        
        Returns:
            Career overview with all key metrics
        """
        # Get all data
        skills_result = self.get_skills_inventory()
        goals_result = self.list_learning_goals()
        portfolio_result = self.get_portfolio()
        rate_result = self.get_rate_history()
        network_result = self.list_network_contacts()
        
        milestones = self._get_collection("milestones")
        milestone_list = sorted(
            milestones.values(),
            key=lambda m: m.get("achieved_date", ""),
            reverse=True
        )
        
        return {
            "skills": {
                "total": skills_result.get("summary", {}).get("total_skills", 0),
                "average_proficiency": skills_result.get("summary", {}).get("average_proficiency", 0),
                "by_category": skills_result.get("summary", {}).get("by_category", {})
            },
            "learning": {
                "active_goals": goals_result.get("summary", {}).get("by_status", {}).get("in_progress", 0),
                "completed_goals": goals_result.get("summary", {}).get("by_status", {}).get("completed", 0),
                "average_progress": goals_result.get("summary", {}).get("average_progress", 0)
            },
            "portfolio": {
                "project_count": portfolio_result.get("count", 0)
            },
            "rates": {
                "current": rate_result.get("current_rate"),
                "growth_percent": rate_result.get("growth_percent", 0)
            },
            "network": {
                "total_contacts": network_result.get("summary", {}).get("total_contacts", 0),
                "by_relationship": network_result.get("summary", {}).get("by_relationship", {})
            },
            "milestones": {
                "total": len(milestone_list),
                "recent": milestone_list[:5]
            }
        }


# Standalone functions for MCP tool interface
_server_instance = None

def _get_server() -> CareerServer:
    """Get or create server instance."""
    global _server_instance
    if _server_instance is None:
        _server_instance = CareerServer()
    return _server_instance


def add_skill(**kwargs) -> dict:
    """Add a skill."""
    return _get_server().add_skill(**kwargs)


def update_skill_level(**kwargs) -> dict:
    """Update skill level."""
    return _get_server().update_skill_level(**kwargs)


def get_skills_inventory(**kwargs) -> dict:
    """Get skills inventory."""
    return _get_server().get_skills_inventory(**kwargs)


def identify_skill_gaps(**kwargs) -> dict:
    """Identify skill gaps."""
    return _get_server().identify_skill_gaps(**kwargs)


def create_learning_goal(**kwargs) -> dict:
    """Create learning goal."""
    return _get_server().create_learning_goal(**kwargs)


def update_learning_progress(**kwargs) -> dict:
    """Update learning progress."""
    return _get_server().update_learning_progress(**kwargs)


def list_learning_goals(**kwargs) -> dict:
    """List learning goals."""
    return _get_server().list_learning_goals(**kwargs)


def add_portfolio_project(**kwargs) -> dict:
    """Add portfolio project."""
    return _get_server().add_portfolio_project(**kwargs)


def get_portfolio(**kwargs) -> dict:
    """Get portfolio."""
    return _get_server().get_portfolio(**kwargs)


def record_rate_change(**kwargs) -> dict:
    """Record rate change."""
    return _get_server().record_rate_change(**kwargs)


def get_rate_history(**kwargs) -> dict:
    """Get rate history."""
    return _get_server().get_rate_history(**kwargs)


def add_network_contact(**kwargs) -> dict:
    """Add network contact."""
    return _get_server().add_network_contact(**kwargs)


def list_network_contacts(**kwargs) -> dict:
    """List network contacts."""
    return _get_server().list_network_contacts(**kwargs)


def add_milestone(**kwargs) -> dict:
    """Add career milestone."""
    return _get_server().add_milestone(**kwargs)


def get_career_summary() -> dict:
    """Get career summary."""
    return _get_server().get_career_summary()


def get_server_info() -> dict:
    """Get server info."""
    return _get_server().get_info()


if __name__ == "__main__":
    server = CareerServer()
    print("Career Server - Career Development & Skills Tracking MCP Server")
    print(f"Data file: {server.data_path}")
    info = server.get_info()
    print(f"Available tools: {', '.join(info['tools'])}")
