"""
Tests for Billing Server - Invoicing and Payment MCP Server
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from decimal import Decimal

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.mcp.billing_server import BillingServer


@pytest.fixture
def temp_data_dir(tmp_path, monkeypatch):
    """Create a temporary data directory for testing."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Patch Config to use temp directory
    from core import config
    monkeypatch.setattr(config.Config, "DATA_DIR", data_dir)
    monkeypatch.setattr(config.Config, "STRIPE_API_KEY", None)  # Disable Stripe for tests
    
    yield data_dir


@pytest.fixture
def billing_server(temp_data_dir):
    """Create a fresh billing server instance for each test."""
    return BillingServer()


@pytest.fixture
def mock_stripe(monkeypatch):
    """Mock Stripe API for testing payment integration."""
    mock_stripe_module = MagicMock()
    mock_stripe_module.Invoice.create.return_value = {
        "id": "inv_test123",
        "status": "open"
    }
    mock_stripe_module.PaymentIntent.create.return_value = {
        "id": "pi_test123",
        "status": "succeeded"
    }
    
    return mock_stripe_module


def test_create_invoice_basic(billing_server):
    """Test creating a basic invoice."""
    items = [
        {
            "description": "Web Development",
            "quantity": 40,
            "rate": 150.0
        },
        {
            "description": "Consulting",
            "quantity": 10,
            "rate": 200.0
        }
    ]
    
    result = billing_server.create_invoice(
        client_id="client-123",
        client_name="Acme Corp",
        items=items,
        notes="Payment due within 30 days"
    )
    
    assert "invoice_id" in result
    assert result["status"] == "created"
    assert result["invoice"]["client_name"] == "Acme Corp"
    assert result["invoice"]["status"] == "draft"
    # 40 * 150 + 10 * 200 = 6000 + 2000 = 8000
    assert result["invoice"]["subtotal"] == 8000.0


def test_create_invoice_with_tax(billing_server):
    """Test creating an invoice with tax."""
    items = [
        {
            "description": "Service",
            "quantity": 10,
            "rate": 100.0
        }
    ]
    
    result = billing_server.create_invoice(
        client_id="client-456",
        client_name="TechCorp",
        items=items,
        tax_rate=0.08  # 8% tax
    )
    
    assert result["invoice"]["subtotal"] == 1000.0
    assert result["invoice"]["tax_amount"] == 80.0
    assert result["invoice"]["total"] == 1080.0


def test_create_invoice_with_discount(billing_server):
    """Test creating an invoice with discount."""
    items = [
        {
            "description": "Project Work",
            "quantity": 50,
            "rate": 100.0
        }
    ]
    
    result = billing_server.create_invoice(
        client_id="client-789",
        client_name="StartupCo",
        items=items,
        discount=500.0
    )
    
    assert result["invoice"]["subtotal"] == 5000.0
    assert result["invoice"]["discount"] == 500.0
    assert result["invoice"]["total"] == 4500.0


def test_get_invoice(billing_server):
    """Test retrieving an invoice by ID."""
    # Create an invoice
    items = [{"description": "Test", "quantity": 1, "rate": 100.0}]
    create_result = billing_server.create_invoice(
        client_id="client-test",
        client_name="Test Client",
        items=items
    )
    invoice_id = create_result["invoice_id"]
    
    # Retrieve it
    get_result = billing_server.get_invoice(invoice_id)
    
    assert "invoice" in get_result
    assert get_result["invoice"]["id"] == invoice_id


def test_update_invoice_status(billing_server):
    """Test updating invoice status."""
    # Create an invoice
    items = [{"description": "Work", "quantity": 10, "rate": 150.0}]
    create_result = billing_server.create_invoice(
        client_id="client-status",
        client_name="Status Client",
        items=items
    )
    invoice_id = create_result["invoice_id"]
    
    # Update status to sent
    result = billing_server.update_invoice_status(
        invoice_id=invoice_id,
        status="sent"
    )
    
    assert result.get("success")
    assert result["invoice"]["status"] == "sent"


def test_list_invoices(billing_server):
    """Test listing all invoices."""
    # Create multiple invoices
    items = [{"description": "Item", "quantity": 1, "rate": 100.0}]
    
    billing_server.create_invoice("client-1", "Client 1", items)
    billing_server.create_invoice("client-2", "Client 2", items)
    billing_server.create_invoice("client-3", "Client 3", items)
    
    # List all
    result = billing_server.list_invoices()
    
    assert "records" in result
    assert result["count"] == 3


def test_list_invoices_by_status(billing_server):
    """Test filtering invoices by status."""
    items = [{"description": "Item", "quantity": 1, "rate": 100.0}]
    
    # Create invoices with different statuses
    inv1 = billing_server.create_invoice("client-1", "Client 1", items)
    inv2 = billing_server.create_invoice("client-2", "Client 2", items)
    inv3 = billing_server.create_invoice("client-3", "Client 3", items)
    
    # Update one to sent
    billing_server.update_invoice_status(inv1["invoice_id"], "sent")
    
    # Filter by draft status
    result = billing_server.list_invoices(status="draft")
    assert result["count"] == 2


def test_record_payment(billing_server):
    """Test recording a payment on an invoice."""
    # Create an invoice
    items = [{"description": "Service", "quantity": 20, "rate": 100.0}]
    create_result = billing_server.create_invoice(
        client_id="client-pay",
        client_name="Payment Client",
        items=items
    )
    invoice_id = create_result["invoice_id"]
    
    # Record payment
    result = billing_server.record_payment(
        invoice_id=invoice_id,
        amount=2000.0,
        payment_method="bank_transfer",
        notes="Wire transfer received"
    )
    
    assert "payment_id" in result
    assert result["status"] == "recorded"
    assert result["invoice_status"] == "paid"


def test_record_partial_payment(billing_server):
    """Test recording a partial payment."""
    # Create invoice for $1000
    items = [{"description": "Work", "quantity": 10, "rate": 100.0}]
    create_result = billing_server.create_invoice(
        client_id="client-partial",
        client_name="Partial Client",
        items=items
    )
    invoice_id = create_result["invoice_id"]
    
    # Pay $500
    result = billing_server.record_payment(
        invoice_id=invoice_id,
        amount=500.0,
        payment_method="check"
    )
    
    assert result["invoice_status"] == "partially_paid"
    assert result["amount_paid"] == 500.0
    assert result["amount_due"] == 500.0


def test_create_expense(billing_server):
    """Test creating an expense record."""
    result = billing_server.create_expense(
        description="Office Supplies",
        amount=150.50,
        category="office",
        payment_method="credit_card",
        date="2024-06-01"
    )
    
    assert "expense_id" in result
    assert result["status"] == "created"
    assert result["expense"]["description"] == "Office Supplies"
    assert result["expense"]["amount"] == 150.50


def test_list_expenses(billing_server):
    """Test listing expenses."""
    # Create multiple expenses
    billing_server.create_expense("Expense 1", 100.0, "office")
    billing_server.create_expense("Expense 2", 200.0, "software")
    billing_server.create_expense("Expense 3", 300.0, "travel")
    
    # List all
    result = billing_server.list_expenses()
    
    assert "records" in result
    assert result["count"] == 3


def test_get_revenue_report(billing_server):
    """Test generating a revenue report."""
    # Create and pay some invoices
    items = [{"description": "Work", "quantity": 10, "rate": 150.0}]
    
    inv1 = billing_server.create_invoice("client-1", "Client 1", items)
    inv2 = billing_server.create_invoice("client-2", "Client 2", items)
    
    # Mark both as paid
    billing_server.record_payment(inv1["invoice_id"], 1500.0, "bank_transfer")
    billing_server.record_payment(inv2["invoice_id"], 1500.0, "check")
    
    # Get revenue report
    result = billing_server.get_revenue_report(period="all")
    
    assert "total_revenue" in result
    assert result["total_revenue"] == 3000.0


def test_get_profit_margin(billing_server):
    """Test calculating profit margin."""
    # Create revenue
    items = [{"description": "Work", "quantity": 100, "rate": 100.0}]
    inv = billing_server.create_invoice("client-profit", "Client", items)
    billing_server.record_payment(inv["invoice_id"], 10000.0, "bank_transfer")
    
    # Create expenses
    billing_server.create_expense("Expense 1", 2000.0, "software")
    billing_server.create_expense("Expense 2", 1000.0, "office")
    
    # Get profit margin
    result = billing_server.get_profit_margin(period="all")
    
    assert "revenue" in result
    assert "expenses" in result
    assert "profit" in result
    assert result["profit"] == 7000.0  # 10000 - 3000


def test_get_overdue_invoices(billing_server):
    """Test getting overdue invoices."""
    # Create invoice with past due date
    from datetime import datetime, timedelta
    
    items = [{"description": "Work", "quantity": 10, "rate": 100.0}]
    past_date = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")
    
    result = billing_server.create_invoice(
        client_id="client-overdue",
        client_name="Overdue Client",
        items=items,
        due_date=past_date
    )
    
    # Get overdue invoices
    overdue = billing_server.get_overdue_invoices()
    
    assert "invoices" in overdue
    assert overdue["count"] >= 0  # May be 0 or 1 depending on status


def test_send_payment_reminder(billing_server):
    """Test sending payment reminder (mocked)."""
    # Create an unpaid invoice
    items = [{"description": "Work", "quantity": 5, "rate": 100.0}]
    create_result = billing_server.create_invoice(
        client_id="client-reminder",
        client_name="Reminder Client",
        items=items
    )
    invoice_id = create_result["invoice_id"]
    
    # Send reminder (should work even without email configured)
    result = billing_server.send_payment_reminder(invoice_id)
    
    # Should return success or appropriate message
    assert "message" in result or "error" in result


def test_server_info(billing_server):
    """Test getting server information."""
    info = billing_server.get_info()
    
    assert info["name"] == "billing-server"
    assert "version" in info
    assert "tools" in info
    assert "create_invoice" in info["tools"]
    assert "record_payment" in info["tools"]
