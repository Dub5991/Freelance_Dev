"""
Tests for LLC Ops Server - Business Operations and Compliance MCP Server
"""

import pytest
from pathlib import Path
from datetime import datetime, date

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.mcp.llc_ops_server import LLCOpsServer


@pytest.fixture
def temp_data_dir(tmp_path, monkeypatch):
    """Create a temporary data directory for testing."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Patch Config to use temp directory
    from core import config
    monkeypatch.setattr(config.Config, "DATA_DIR", data_dir)
    monkeypatch.setattr(config.Config, "LLC_NAME", "Test LLC")
    monkeypatch.setattr(config.Config, "LLC_EIN", "12-3456789")
    monkeypatch.setattr(config.Config, "LLC_STATE", "CA")
    
    yield data_dir


@pytest.fixture
def llc_ops_server(temp_data_dir):
    """Create a fresh LLC ops server instance for each test."""
    return LLCOpsServer()


def test_get_entity_info(llc_ops_server):
    """Test getting LLC entity information."""
    result = llc_ops_server.get_entity_info()
    
    assert "entity" in result
    assert result["entity"]["llc_name"] == "Test LLC"
    assert result["entity"]["ein"] == "12-3456789"
    assert result["entity"]["state"] == "CA"


def test_update_entity_info(llc_ops_server):
    """Test updating LLC entity information."""
    result = llc_ops_server.update_entity_info(
        formation_date="2023-01-15",
        tax_classification="s_corp"
    )
    
    assert "entity" in result
    assert result["entity"]["formation_date"] == "2023-01-15"
    assert result["entity"]["tax_classification"] == "s_corp"


def test_get_tax_deadlines(llc_ops_server):
    """Test getting tax deadlines."""
    result = llc_ops_server.get_tax_deadlines()
    
    assert "deadlines" in result
    # Should have quarterly estimates and annual return
    assert result["count"] >= 5


def test_calculate_quarterly_estimate_basic(llc_ops_server):
    """Test calculating quarterly tax estimate."""
    result = llc_ops_server.calculate_quarterly_estimate(
        quarter=1,
        year=2024,
        gross_income=50000.0,
        business_expenses=10000.0
    )
    
    assert "quarter" in result
    assert "estimated_tax" in result
    assert "net_income" in result
    assert result["net_income"] == 40000.0  # 50000 - 10000


def test_calculate_quarterly_estimate_with_deductions(llc_ops_server):
    """Test quarterly estimate with standard deduction."""
    result = llc_ops_server.calculate_quarterly_estimate(
        quarter=2,
        year=2024,
        gross_income=60000.0,
        business_expenses=15000.0,
        self_employment_tax=True
    )
    
    assert result["net_income"] == 45000.0
    assert "self_employment_tax" in result
    assert "estimated_tax" in result


def test_add_compliance_item(llc_ops_server):
    """Test adding a compliance checklist item."""
    result = llc_ops_server.add_compliance_item(
        title="File Annual Report",
        due_date="2024-12-31",
        description="Submit annual report to state",
        category="state_filing"
    )
    
    assert "item_id" in result
    assert result["status"] == "created"
    assert result["item"]["title"] == "File Annual Report"
    assert result["item"]["completed"] is False


def test_get_compliance_checklist(llc_ops_server):
    """Test getting compliance checklist."""
    # Add some items
    llc_ops_server.add_compliance_item(
        "Item 1",
        "2024-06-30",
        category="tax"
    )
    llc_ops_server.add_compliance_item(
        "Item 2",
        "2024-09-30",
        category="state_filing"
    )
    
    # Get checklist
    result = llc_ops_server.get_compliance_checklist()
    
    assert "items" in result
    assert result["count"] >= 2


def test_complete_compliance_item(llc_ops_server):
    """Test completing a compliance item."""
    # Add an item
    add_result = llc_ops_server.add_compliance_item(
        "Test Compliance Task",
        "2024-08-15"
    )
    item_id = add_result["item_id"]
    
    # Complete it
    result = llc_ops_server.complete_compliance_item(
        item_id=item_id,
        notes="Filed successfully"
    )
    
    assert result.get("success")
    assert result["item"]["completed"] is True
    assert result["item"]["completion_notes"] == "Filed successfully"


def test_upload_document(llc_ops_server):
    """Test uploading a document record."""
    result = llc_ops_server.upload_document(
        name="Operating Agreement",
        document_type="legal",
        file_path="/vault/docs/operating_agreement.pdf",
        description="Updated operating agreement 2024"
    )
    
    assert "document_id" in result
    assert result["status"] == "uploaded"
    assert result["document"]["name"] == "Operating Agreement"


def test_list_documents(llc_ops_server):
    """Test listing documents."""
    # Upload some documents
    llc_ops_server.upload_document(
        "Doc 1",
        "tax",
        "/path/doc1.pdf"
    )
    llc_ops_server.upload_document(
        "Doc 2",
        "legal",
        "/path/doc2.pdf"
    )
    
    # List all
    result = llc_ops_server.list_documents()
    
    assert "records" in result
    assert result["count"] >= 2


def test_list_documents_by_type(llc_ops_server):
    """Test filtering documents by type."""
    # Upload documents of different types
    llc_ops_server.upload_document("Tax Doc", "tax", "/path/tax.pdf")
    llc_ops_server.upload_document("Legal Doc", "legal", "/path/legal.pdf")
    
    # Filter by type
    result = llc_ops_server.list_documents(document_type="tax")
    
    # Should have at least the tax document
    tax_docs = [d for d in result["records"] if d.get("document_type") == "tax"]
    assert len(tax_docs) >= 1


def test_get_tax_summary(llc_ops_server):
    """Test getting tax summary."""
    result = llc_ops_server.get_tax_summary(year=2024)
    
    assert "year" in result
    assert "quarterly_estimates" in result
    assert "annual_deadline" in result


def test_server_info(llc_ops_server):
    """Test getting server information."""
    info = llc_ops_server.get_info()
    
    assert info["name"] == "llc-ops-server"
    assert "version" in info
    assert "tools" in info
    assert "calculate_quarterly_estimate" in info["tools"]
    assert "get_compliance_checklist" in info["tools"]


def test_server_health_check(llc_ops_server):
    """Test server health check."""
    health = llc_ops_server.health_check()
    
    assert "healthy" in health
    assert health["server"] == "llc_ops"


def test_quarterly_estimates_for_full_year(llc_ops_server):
    """Test calculating estimates for all four quarters."""
    quarterly_income = 25000.0
    quarterly_expenses = 5000.0
    
    for quarter in range(1, 5):
        result = llc_ops_server.calculate_quarterly_estimate(
            quarter=quarter,
            year=2024,
            gross_income=quarterly_income,
            business_expenses=quarterly_expenses
        )
        
        assert result["quarter"] == quarter
        assert result["net_income"] == 20000.0
        assert "estimated_tax" in result


def test_compliance_by_category(llc_ops_server):
    """Test getting compliance items by category."""
    # Add items in different categories
    llc_ops_server.add_compliance_item("Tax Item", "2024-04-15", category="tax")
    llc_ops_server.add_compliance_item("State Item", "2024-06-30", category="state_filing")
    llc_ops_server.add_compliance_item("License Item", "2024-12-31", category="license")
    
    # Get checklist and verify categories
    result = llc_ops_server.get_compliance_checklist()
    
    categories = set(item.get("category") for item in result["items"])
    assert "tax" in categories
    assert "state_filing" in categories
    assert "license" in categories
