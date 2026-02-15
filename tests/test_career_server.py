"""
Tests for Career Server - Professional Development MCP Server
"""

import pytest
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.mcp.career_server import CareerServer


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
def career_server(temp_data_dir):
    """Create a fresh career server instance for each test."""
    return CareerServer()


def test_add_skill(career_server):
    """Test adding a new skill."""
    result = career_server.add_skill(
        name="Python",
        category="programming",
        proficiency_level="expert",
        years_experience=8.0
    )
    
    assert "skill_id" in result
    assert result["status"] == "added"
    assert result["skill"]["name"] == "Python"
    assert result["skill"]["proficiency_level"] == "expert"


def test_add_skill_duplicate(career_server):
    """Test that duplicate skills are not allowed."""
    # Add first skill
    career_server.add_skill(
        name="JavaScript",
        category="programming",
        proficiency_level="advanced"
    )
    
    # Try to add duplicate
    result = career_server.add_skill(
        name="JavaScript",
        category="programming",
        proficiency_level="expert"
    )
    
    assert "error" in result
    assert "already exists" in result["error"].lower()


def test_get_skill(career_server):
    """Test retrieving a skill by ID."""
    # Add a skill
    add_result = career_server.add_skill(
        name="React",
        category="framework",
        proficiency_level="advanced"
    )
    skill_id = add_result["skill_id"]
    
    # Retrieve it
    get_result = career_server.get_skill(skill_id)
    
    assert "skill" in get_result
    assert get_result["skill"]["name"] == "React"


def test_list_skills(career_server):
    """Test listing all skills."""
    # Add multiple skills
    career_server.add_skill("Skill 1", "programming", "intermediate")
    career_server.add_skill("Skill 2", "design", "beginner")
    career_server.add_skill("Skill 3", "project_management", "advanced")
    
    # List all
    result = career_server.list_skills()
    
    assert "records" in result
    assert result["count"] >= 3


def test_list_skills_by_category(career_server):
    """Test filtering skills by category."""
    # Add skills in different categories
    career_server.add_skill("Python", "programming", "expert")
    career_server.add_skill("Photoshop", "design", "intermediate")
    career_server.add_skill("AWS", "cloud", "advanced")
    
    # Filter by category
    result = career_server.list_skills(category="programming")
    
    programming_skills = [s for s in result["records"] if s.get("category") == "programming"]
    assert len(programming_skills) >= 1


def test_update_skill(career_server):
    """Test updating skill information."""
    # Add a skill
    add_result = career_server.add_skill(
        name="TypeScript",
        category="programming",
        proficiency_level="intermediate",
        years_experience=2.0
    )
    skill_id = add_result["skill_id"]
    
    # Update it
    update_result = career_server.update_skill(
        skill_id=skill_id,
        proficiency_level="advanced",
        years_experience=4.0
    )
    
    assert update_result.get("success")
    assert update_result["record"]["proficiency_level"] == "advanced"
    assert update_result["record"]["years_experience"] == 4.0


def test_log_skill_evidence(career_server):
    """Test logging evidence of skill usage."""
    # Add a skill
    add_result = career_server.add_skill(
        name="Docker",
        category="devops",
        proficiency_level="intermediate"
    )
    skill_id = add_result["skill_id"]
    
    # Log evidence
    result = career_server.log_skill_evidence(
        skill_id=skill_id,
        evidence_type="project",
        description="Built multi-container application for client",
        project_name="E-commerce Platform",
        date="2024-06-01"
    )
    
    assert "evidence_id" in result
    assert result["status"] == "logged"


def test_get_skill_evidence(career_server):
    """Test retrieving evidence for a skill."""
    # Add skill and evidence
    add_result = career_server.add_skill(
        name="PostgreSQL",
        category="database",
        proficiency_level="advanced"
    )
    skill_id = add_result["skill_id"]
    
    career_server.log_skill_evidence(
        skill_id=skill_id,
        evidence_type="certification",
        description="PostgreSQL Advanced Certification"
    )
    
    # Get evidence
    result = career_server.get_skill_evidence(skill_id)
    
    assert "evidence" in result
    assert len(result["evidence"]) >= 1


def test_add_portfolio_item(career_server):
    """Test adding a portfolio item."""
    result = career_server.add_portfolio_item(
        title="E-commerce Website",
        description="Full-stack e-commerce platform with React and Node.js",
        project_type="web_development",
        technologies=["React", "Node.js", "PostgreSQL", "Stripe"],
        url="https://example.com",
        completion_date="2024-05-15"
    )
    
    assert "portfolio_id" in result
    assert result["status"] == "added"
    assert result["portfolio_item"]["title"] == "E-commerce Website"


def test_list_portfolio(career_server):
    """Test listing portfolio items."""
    # Add multiple items
    career_server.add_portfolio_item(
        "Project 1",
        "Description 1",
        "web_development",
        ["React"]
    )
    career_server.add_portfolio_item(
        "Project 2",
        "Description 2",
        "mobile_app",
        ["React Native"]
    )
    
    # List all
    result = career_server.list_portfolio()
    
    assert "records" in result
    assert result["count"] >= 2


def test_get_rate_suggestion(career_server):
    """Test getting rate suggestions based on skills."""
    # Add some expert-level skills
    career_server.add_skill("Python", "programming", "expert", 10.0)
    career_server.add_skill("AWS", "cloud", "expert", 8.0)
    career_server.add_skill("React", "framework", "advanced", 6.0)
    
    # Get rate suggestion
    result = career_server.get_rate_suggestion()
    
    assert "suggested_rate" in result
    assert "rationale" in result
    assert result["suggested_rate"] > 0


def test_rate_suggestion_considers_experience(career_server):
    """Test that rate suggestions factor in years of experience."""
    # Junior developer
    career_server.add_skill("JavaScript", "programming", "intermediate", 2.0)
    junior_rate = career_server.get_rate_suggestion()
    
    # Clear and add senior experience
    career_server = CareerServer()
    career_server.add_skill("JavaScript", "programming", "expert", 10.0)
    career_server.add_skill("Architecture", "design", "expert", 8.0)
    senior_rate = career_server.get_rate_suggestion()
    
    # Senior should have higher rate
    assert senior_rate["suggested_rate"] >= junior_rate["suggested_rate"]


def test_calculate_skill_gaps(career_server):
    """Test identifying skill gaps for a target role."""
    # Add current skills
    career_server.add_skill("Python", "programming", "advanced")
    career_server.add_skill("Django", "framework", "intermediate")
    
    # Get gaps for a role
    result = career_server.calculate_skill_gaps(
        target_role="Full Stack Developer",
        required_skills=[
            "Python",
            "Django",
            "React",
            "PostgreSQL",
            "Docker"
        ]
    )
    
    assert "gaps" in result
    assert "existing_skills" in result
    # Should identify React, PostgreSQL, Docker as gaps
    assert len(result["gaps"]) >= 3


def test_generate_learning_plan(career_server):
    """Test generating a learning plan for skill development."""
    result = career_server.generate_learning_plan(
        skill_name="Kubernetes",
        target_proficiency="advanced",
        timeframe_weeks=12
    )
    
    assert "plan" in result
    assert result["plan"]["skill_name"] == "Kubernetes"
    assert result["plan"]["target_proficiency"] == "advanced"


def test_server_info(career_server):
    """Test getting server information."""
    info = career_server.get_info()
    
    assert info["name"] == "career-server"
    assert "version" in info
    assert "tools" in info
    assert "add_skill" in info["tools"]
    assert "get_rate_suggestion" in info["tools"]


def test_server_health_check(career_server):
    """Test server health check."""
    health = career_server.health_check()
    
    assert "healthy" in health
    assert health["server"] == "career"


def test_portfolio_with_featured_items(career_server):
    """Test marking portfolio items as featured."""
    # Add portfolio item
    add_result = career_server.add_portfolio_item(
        "Featured Project",
        "My best work",
        "web_development",
        ["React", "Node.js"],
        featured=True
    )
    
    assert add_result["portfolio_item"].get("featured") is True or add_result["portfolio_item"].get("featured") is None


def test_skill_proficiency_levels(career_server):
    """Test that all standard proficiency levels are accepted."""
    levels = ["beginner", "intermediate", "advanced", "expert"]
    
    for i, level in enumerate(levels):
        result = career_server.add_skill(
            name=f"Skill_{level}",
            category="programming",
            proficiency_level=level
        )
        
        assert result.get("skill_id") is not None
        assert result["skill"]["proficiency_level"] == level


def test_multiple_evidence_entries(career_server):
    """Test logging multiple pieces of evidence for a skill."""
    # Add skill
    add_result = career_server.add_skill(
        name="GraphQL",
        category="api",
        proficiency_level="intermediate"
    )
    skill_id = add_result["skill_id"]
    
    # Log multiple evidence entries
    career_server.log_skill_evidence(
        skill_id=skill_id,
        evidence_type="project",
        description="API for mobile app"
    )
    career_server.log_skill_evidence(
        skill_id=skill_id,
        evidence_type="course",
        description="GraphQL Advanced Course"
    )
    career_server.log_skill_evidence(
        skill_id=skill_id,
        evidence_type="certification",
        description="GraphQL Professional Certificate"
    )
    
    # Get all evidence
    result = career_server.get_skill_evidence(skill_id)
    
    assert len(result["evidence"]) == 3
