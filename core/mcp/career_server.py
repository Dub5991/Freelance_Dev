"""
Career Server - MCP Server for Career Development Tracking

Full async implementation for:
- Skill development tracking
- Evidence capture
- Portfolio building
- Rate optimization suggestions
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
CAREER_PATH = Path(VAULT_PATH) / "05-Areas" / "Career"
SKILLS_PATH = CAREER_PATH / "skills"
PORTFOLIO_PATH = CAREER_PATH / "portfolio"


class CareerServer:
    """Async MCP Server for career development tracking"""
    
    def __init__(self):
        self.server = Server("career-server")
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup all tool handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="add_skill",
                    description="Add or update a skill",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Skill name"},
                            "category": {
                                "type": "string",
                                "enum": [
                                    "Programming Language", "Framework", "Tool",
                                    "Cloud Platform", "Database", "Methodology",
                                    "Soft Skill", "Domain Knowledge"
                                ],
                                "description": "Skill category"
                            },
                            "proficiency": {
                                "type": "string",
                                "enum": ["Beginner", "Intermediate", "Advanced", "Expert"],
                                "description": "Current proficiency level"
                            },
                            "years_experience": {"type": "number", "description": "Years of experience"},
                            "last_used": {"type": "string", "description": "Last used date YYYY-MM-DD"}
                        },
                        "required": ["name", "category", "proficiency"]
                    }
                ),
                Tool(
                    name="log_evidence",
                    description="Log evidence of skill application",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "skill_name": {"type": "string", "description": "Related skill"},
                            "project": {"type": "string", "description": "Project/client name"},
                            "description": {"type": "string", "description": "What you did"},
                            "impact": {"type": "string", "description": "Business impact/results"},
                            "date": {"type": "string", "description": "Date YYYY-MM-DD"}
                        },
                        "required": ["skill_name", "project", "description"]
                    }
                ),
                Tool(
                    name="get_portfolio",
                    description="Get portfolio items for showcasing work",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "skill": {"type": "string", "description": "Filter by skill"},
                            "category": {"type": "string", "description": "Filter by category"},
                            "top_n": {"type": "number", "description": "Return top N items"}
                        }
                    }
                ),
                Tool(
                    name="suggest_rate",
                    description="Get rate optimization suggestions based on skills and market",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "current_rate": {"type": "number", "description": "Current hourly rate"}
                        },
                        "required": ["current_rate"]
                    }
                ),
                Tool(
                    name="list_skills",
                    description="List all tracked skills",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "category": {"type": "string", "description": "Filter by category"},
                            "min_proficiency": {
                                "type": "string",
                                "enum": ["Beginner", "Intermediate", "Advanced", "Expert"],
                                "description": "Minimum proficiency level"
                            }
                        }
                    }
                ),
                Tool(
                    name="get_skill_gaps",
                    description="Identify skill gaps based on strategic pillars",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Route tool calls to appropriate handlers"""
            
            if name == "add_skill":
                result = await self._add_skill(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "log_evidence":
                result = await self._log_evidence(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "get_portfolio":
                result = await self._get_portfolio(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "suggest_rate":
                result = await self._suggest_rate(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "list_skills":
                result = await self._list_skills(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "get_skill_gaps":
                result = await self._get_skill_gaps()
                return [TextContent(type="text", text=str(result))]
            
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def _add_skill(
        self,
        name: str,
        category: str,
        proficiency: str,
        years_experience: float = 0,
        last_used: str = None
    ) -> Dict[str, Any]:
        """Add or update a skill"""
        
        SKILLS_PATH.mkdir(parents=True, exist_ok=True)
        
        skill_id = name.lower().replace(" ", "-").replace("/", "-")
        skill_file = SKILLS_PATH / f"{skill_id}.yaml"
        
        # Load existing or create new
        if skill_file.exists():
            with open(skill_file, 'r') as f:
                skill = yaml.safe_load(f)
            message = f"Skill '{name}' updated"
        else:
            skill = {
                "skill_id": skill_id,
                "name": name,
                "created_at": datetime.now().isoformat()
            }
            message = f"Skill '{name}' added"
        
        # Update fields
        skill.update({
            "category": category,
            "proficiency": proficiency,
            "years_experience": years_experience,
            "last_used": last_used or datetime.now().date().isoformat(),
            "updated_at": datetime.now().isoformat()
        })
        
        # Save
        with open(skill_file, 'w') as f:
            yaml.safe_dump(skill, f, default_flow_style=False, sort_keys=False)
        
        return {
            "success": True,
            "skill_id": skill_id,
            "message": message
        }
    
    async def _log_evidence(
        self,
        skill_name: str,
        project: str,
        description: str,
        impact: str = "",
        date: str = None
    ) -> Dict[str, Any]:
        """Log evidence of skill application"""
        
        # Find skill
        skill_id = skill_name.lower().replace(" ", "-").replace("/", "-")
        skill_file = SKILLS_PATH / f"{skill_id}.yaml"
        
        if not skill_file.exists():
            return {
                "success": False,
                "error": f"Skill '{skill_name}' not found. Add it first with add_skill."
            }
        
        # Load skill
        with open(skill_file, 'r') as f:
            skill = yaml.safe_load(f)
        
        # Add evidence
        if "evidence" not in skill:
            skill["evidence"] = []
        
        evidence = {
            "project": project,
            "description": description,
            "impact": impact,
            "date": date or datetime.now().date().isoformat(),
            "logged_at": datetime.now().isoformat()
        }
        
        skill["evidence"].append(evidence)
        skill["updated_at"] = datetime.now().isoformat()
        skill["last_used"] = evidence["date"]
        
        # Save
        with open(skill_file, 'w') as f:
            yaml.safe_dump(skill, f, default_flow_style=False, sort_keys=False)
        
        # Also save to portfolio
        await self._add_to_portfolio(skill_name, evidence)
        
        return {
            "success": True,
            "message": f"Evidence logged for {skill_name}",
            "total_evidence": len(skill["evidence"])
        }
    
    async def _get_portfolio(
        self,
        skill: str = None,
        category: str = None,
        top_n: int = None
    ) -> Dict[str, Any]:
        """Get portfolio items"""
        
        if not PORTFOLIO_PATH.exists():
            return {"success": True, "count": 0, "items": []}
        
        items = []
        for portfolio_file in PORTFOLIO_PATH.glob("*.yaml"):
            with open(portfolio_file, 'r') as f:
                item = yaml.safe_load(f)
                if not item:
                    continue
                
                # Apply filters
                if skill and item.get("skill") != skill:
                    continue
                if category and item.get("category") != category:
                    continue
                
                items.append(item)
        
        # Sort by date (most recent first)
        items.sort(key=lambda i: i.get("date", ""), reverse=True)
        
        # Limit results
        if top_n:
            items = items[:top_n]
        
        return {
            "success": True,
            "count": len(items),
            "items": items
        }
    
    async def _suggest_rate(self, current_rate: float) -> Dict[str, Any]:
        """Suggest rate optimization"""
        
        # Load all skills
        skills = await self._load_all_skills()
        
        if not skills:
            return {
                "success": True,
                "current_rate": current_rate,
                "suggested_rate": current_rate,
                "message": "Add skills to get rate suggestions"
            }
        
        # Calculate skill score
        proficiency_scores = {
            "Beginner": 1,
            "Intermediate": 2,
            "Advanced": 3,
            "Expert": 4
        }
        
        # Count high-value skills
        expert_skills = sum(
            1 for s in skills
            if s.get("proficiency") == "Expert"
        )
        
        advanced_skills = sum(
            1 for s in skills
            if s.get("proficiency") in ["Advanced", "Expert"]
        )
        
        total_years = sum(
            s.get("years_experience", 0)
            for s in skills
        )
        
        # Simple rate calculation (can be made more sophisticated)
        base_rate = 100  # Base freelance rate
        
        # Add value for expertise
        rate_boost = (expert_skills * 25) + (advanced_skills * 10)
        
        # Add value for experience
        experience_boost = min(total_years * 5, 100)  # Cap at $100
        
        suggested_rate = base_rate + rate_boost + experience_boost
        
        # Round to nearest $5
        suggested_rate = round(suggested_rate / 5) * 5
        
        # Don't suggest lower than current
        suggested_rate = max(suggested_rate, current_rate)
        
        justification = []
        if expert_skills > 0:
            justification.append(f"{expert_skills} expert-level skills")
        if advanced_skills > 0:
            justification.append(f"{advanced_skills} advanced skills")
        if total_years > 0:
            justification.append(f"{total_years:.1f} years total experience")
        
        return {
            "success": True,
            "current_rate": current_rate,
            "suggested_rate": suggested_rate,
            "increase": suggested_rate - current_rate,
            "increase_percentage": round(((suggested_rate - current_rate) / current_rate * 100), 1) if current_rate > 0 else 0,
            "justification": justification,
            "recommendation": self._get_rate_recommendation(current_rate, suggested_rate)
        }
    
    async def _list_skills(
        self,
        category: str = None,
        min_proficiency: str = None
    ) -> Dict[str, Any]:
        """List all skills"""
        
        skills = await self._load_all_skills()
        
        # Apply filters
        proficiency_order = ["Beginner", "Intermediate", "Advanced", "Expert"]
        min_level = proficiency_order.index(min_proficiency) if min_proficiency else 0
        
        filtered_skills = []
        for skill in skills:
            if category and skill.get("category") != category:
                continue
            
            skill_level = proficiency_order.index(skill.get("proficiency", "Beginner"))
            if skill_level < min_level:
                continue
            
            filtered_skills.append({
                "name": skill["name"],
                "category": skill.get("category"),
                "proficiency": skill.get("proficiency"),
                "years_experience": skill.get("years_experience", 0),
                "evidence_count": len(skill.get("evidence", []))
            })
        
        # Group by category
        by_category = {}
        for skill in filtered_skills:
            cat = skill["category"]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(skill)
        
        return {
            "success": True,
            "count": len(filtered_skills),
            "skills": filtered_skills,
            "by_category": by_category
        }
    
    async def _get_skill_gaps(self) -> Dict[str, Any]:
        """Identify skill gaps"""
        
        # Get strategic pillars from env
        pillars_str = os.getenv("STRATEGIC_PILLARS", "")
        if not pillars_str:
            return {
                "success": False,
                "error": "No strategic pillars defined. Set STRATEGIC_PILLARS in .env"
            }
        
        pillars = [p.strip() for p in pillars_str.split(",")]
        
        # Load skills
        skills = await self._load_all_skills()
        skill_names = [s["name"].lower() for s in skills]
        
        # Define common skills for each pillar (simplified example)
        pillar_skills = {
            "Cloud Architecture": ["AWS", "Azure", "GCP", "Kubernetes", "Terraform"],
            "DevOps": ["CI/CD", "Docker", "Jenkins", "GitHub Actions", "Monitoring"],
            "AI/ML Integration": ["Python", "TensorFlow", "PyTorch", "OpenAI API", "LangChain"],
            "Full Stack": ["React", "Node.js", "PostgreSQL", "REST API", "GraphQL"],
            "Mobile": ["React Native", "Swift", "Kotlin", "Flutter"],
        }
        
        gaps = []
        for pillar in pillars:
            # Find matching pillar skills
            expected_skills = []
            for key, skills_list in pillar_skills.items():
                if key.lower() in pillar.lower():
                    expected_skills = skills_list
                    break
            
            if not expected_skills:
                continue
            
            # Find gaps
            missing = [
                s for s in expected_skills
                if s.lower() not in skill_names
            ]
            
            if missing:
                gaps.append({
                    "pillar": pillar,
                    "missing_skills": missing
                })
        
        return {
            "success": True,
            "strategic_pillars": pillars,
            "gaps": gaps,
            "recommendation": "Focus on developing missing skills aligned with your strategic pillars"
        }
    
    def _get_rate_recommendation(self, current: float, suggested: float) -> str:
        """Get rate change recommendation"""
        
        if suggested <= current:
            return "Your current rate is appropriate. Continue building expertise."
        
        increase_pct = ((suggested - current) / current * 100)
        
        if increase_pct < 5:
            return "Small increase possible. Continue building evidence."
        elif increase_pct < 15:
            return "Moderate increase justified. Prepare case studies for existing clients."
        else:
            return "Significant increase justified. Consider raising rates for new clients first."
    
    async def _add_to_portfolio(self, skill_name: str, evidence: Dict[str, Any]):
        """Add evidence to portfolio"""
        
        PORTFOLIO_PATH.mkdir(parents=True, exist_ok=True)
        
        # Create portfolio item
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        portfolio_id = f"portfolio-{timestamp}"
        
        portfolio_item = {
            "portfolio_id": portfolio_id,
            "skill": skill_name,
            "project": evidence["project"],
            "description": evidence["description"],
            "impact": evidence.get("impact", ""),
            "date": evidence["date"],
            "created_at": datetime.now().isoformat()
        }
        
        # Save
        portfolio_file = PORTFOLIO_PATH / f"{portfolio_id}.yaml"
        with open(portfolio_file, 'w') as f:
            yaml.safe_dump(portfolio_item, f, default_flow_style=False, sort_keys=False)
    
    async def _load_all_skills(self) -> List[Dict[str, Any]]:
        """Load all skills"""
        
        if not SKILLS_PATH.exists():
            return []
        
        skills = []
        for skill_file in SKILLS_PATH.glob("*.yaml"):
            with open(skill_file, 'r') as f:
                skill = yaml.safe_load(f)
                if skill:
                    skills.append(skill)
        
        return skills


async def main():
    """Run the career server"""
    career_server = CareerServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await career_server.server.run(
            read_stream,
            write_stream,
            career_server.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
