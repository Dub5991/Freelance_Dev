"""
Billing Server - Invoicing and Stripe Integration MCP Server

Features:
- Invoice generation and tracking
- Stripe API integration for payments
- Payment status monitoring
- Revenue reporting
- Expense tracking
- Late payment reminders
"""

from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import Optional, List
from ..config import Config
from ..utils import (
    generate_id,
    format_currency,
    format_date,
    round_currency,
    get_quarter,
    get_quarter_dates
)
from .base_server import BaseMCPServer


class BillingServer(BaseMCPServer):
    """Billing and payment management server with Stripe integration."""
    
    def __init__(self):
        super().__init__("billing")
        
        # Initialize collections
        if "invoices" not in self._data:
            self._data["invoices"] = {}
        if "expenses" not in self._data:
            self._data["expenses"] = {}
        if "payments" not in self._data:
            self._data["payments"] = {}
        
        # Initialize Stripe (if available)
        self._stripe_enabled = False
        if Config.STRIPE_API_KEY:
            try:
                import stripe
                stripe.api_key = Config.STRIPE_API_KEY
                self._stripe = stripe
                self._stripe_enabled = True
                self.logger.info("Stripe integration enabled")
            except ImportError:
                self.logger.warning("Stripe module not installed - payment processing disabled")
        else:
            self.logger.info("Stripe API key not configured - running in invoice-only mode")
    
    def get_info(self) -> dict:
        """Return server metadata."""
        return {
            "name": "billing-server",
            "version": "0.1.0",
            "description": "Billing and Stripe integration MCP server",
            "stripe_enabled": self._stripe_enabled,
            "tools": [
                "create_invoice",
                "get_invoice",
                "update_invoice_status",
                "list_invoices",
                "record_payment",
                "create_expense",
                "list_expenses",
                "get_revenue_report",
                "get_profit_margin",
                "send_payment_reminder",
                "get_overdue_invoices"
            ]
        }
    
    def create_invoice(
        self,
        client_id: str,
        client_name: str,
        items: List[dict],
        due_date: Optional[str] = None,
        notes: Optional[str] = None,
        tax_rate: float = 0.0,
        discount: float = 0.0
    ) -> dict:
        """
        Create a new invoice.
        
        Args:
            client_id: Client identifier
            client_name: Client name for invoice
            items: List of invoice items [{"description": str, "quantity": float, "rate": float}]
            due_date: Payment due date (ISO format), defaults to 30 days from now
            notes: Additional notes or payment terms
            tax_rate: Tax rate as decimal (e.g., 0.08 for 8%)
            discount: Discount amount
        
        Returns:
            Invoice with ID and totals
        """
        if not items:
            return {"error": "Invoice must have at least one item"}
        
        # Calculate due date
        if due_date is None:
            due_date = (date.today() + timedelta(days=Config.PAYMENT_TERMS_DAYS)).isoformat()
        
        # Generate invoice ID
        invoice_id = generate_id("inv")
        invoice_number = self._generate_invoice_number()
        
        # Calculate line items and totals
        line_items = []
        subtotal = Decimal('0.00')
        
        for item in items:
            description = item.get("description", "")
            quantity = Decimal(str(item.get("quantity", 1)))
            rate = Decimal(str(item.get("rate", 0)))
            
            line_total = round_currency(quantity * rate)
            subtotal += line_total
            
            line_items.append({
                "description": description,
                "quantity": float(quantity),
                "rate": float(rate),
                "amount": float(line_total)
            })
        
        # Calculate tax and total
        tax_amount = round_currency(subtotal * Decimal(str(tax_rate)))
        discount_amount = round_currency(Decimal(str(discount)))
        total = round_currency(subtotal + tax_amount - discount_amount)
        
        invoice_data = {
            "invoice_number": invoice_number,
            "client_id": client_id,
            "client_name": client_name,
            "line_items": line_items,
            "subtotal": float(subtotal),
            "tax_rate": tax_rate,
            "tax_amount": float(tax_amount),
            "discount": float(discount_amount),
            "total": float(total),
            "currency": Config.DEFAULT_CURRENCY,
            "status": "draft",
            "issue_date": date.today().isoformat(),
            "due_date": due_date,
            "notes": notes or f"Payment due within {Config.PAYMENT_TERMS_DAYS} days",
            "paid_amount": 0.0,
            "paid_date": None,
            "stripe_invoice_id": None,
            "reminders_sent": 0,
            "last_reminder": None
        }
        
        result = self._create_record("invoices", invoice_id, invoice_data)
        
        if result.get("success"):
            self.logger.info(f"Created invoice {invoice_number} for {client_name}: {format_currency(total)}")
            return {
                "invoice_id": invoice_id,
                "invoice_number": invoice_number,
                "status": "created",
                "total": float(total),
                "invoice": result["record"]
            }
        
        return result
    
    def _generate_invoice_number(self) -> str:
        """Generate sequential invoice number."""
        invoices = self._get_collection("invoices")
        
        # Get current year
        year = date.today().year
        year_prefix = str(year)
        
        # Find highest number for this year
        highest = 0
        for inv in invoices.values():
            inv_num = inv.get("invoice_number", "")
            if inv_num.startswith(year_prefix):
                try:
                    num = int(inv_num.split("-")[1])
                    highest = max(highest, num)
                except (IndexError, ValueError):
                    continue
        
        next_num = highest + 1
        return f"{year_prefix}-{next_num:04d}"
    
    def get_invoice(self, invoice_id: str) -> dict:
        """
        Get invoice by ID.
        
        Args:
            invoice_id: Invoice identifier
        
        Returns:
            Invoice details
        """
        result = self._read_record("invoices", invoice_id)
        
        if result.get("success"):
            return {"invoice": result["record"]}
        
        return result
    
    def update_invoice_status(
        self,
        invoice_id: str,
        status: str,
        notes: Optional[str] = None
    ) -> dict:
        """
        Update invoice status.
        
        Args:
            invoice_id: Invoice identifier
            status: New status (draft, sent, paid, overdue, cancelled)
            notes: Optional status change notes
        
        Returns:
            Updated invoice
        """
        valid_statuses = ["draft", "sent", "paid", "overdue", "cancelled"]
        if status not in valid_statuses:
            return {"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}
        
        updates = {"status": status}
        
        if notes:
            updates["status_notes"] = notes
        
        if status == "sent":
            updates["sent_date"] = date.today().isoformat()
        
        result = self._update_record("invoices", invoice_id, updates)
        
        if result.get("success"):
            return {
                "invoice_id": invoice_id,
                "status": status,
                "invoice": result["record"]
            }
        
        return result
    
    def list_invoices(
        self,
        client_id: Optional[str] = None,
        status: Optional[str] = None,
        overdue_only: bool = False
    ) -> dict:
        """
        List invoices with optional filters.
        
        Args:
            client_id: Filter by client
            status: Filter by status
            overdue_only: Show only overdue invoices
        
        Returns:
            List of invoices with summary
        """
        def filter_func(invoice: dict) -> bool:
            if client_id and invoice.get("client_id") != client_id:
                return False
            if status and invoice.get("status") != status:
                return False
            if overdue_only:
                due_date_str = invoice.get("due_date")
                if due_date_str and invoice.get("status") not in ["paid", "cancelled"]:
                    try:
                        due_date_obj = date.fromisoformat(due_date_str)
                        if due_date_obj >= date.today():
                            return False
                    except ValueError:
                        return False
                else:
                    return False
            return True
        
        result = self._list_records("invoices", filter_func, sort_key="issue_date", reverse=True)
        
        if result.get("success"):
            invoices = result["records"]
            
            summary = {
                "total_invoices": len(invoices),
                "by_status": {},
                "total_billed": 0.0,
                "total_paid": 0.0,
                "total_outstanding": 0.0
            }
            
            for invoice in invoices:
                # Status breakdown
                inv_status = invoice.get("status", "unknown")
                summary["by_status"][inv_status] = summary["by_status"].get(inv_status, 0) + 1
                
                # Financial totals
                total = invoice.get("total", 0.0)
                paid = invoice.get("paid_amount", 0.0)
                
                summary["total_billed"] += total
                summary["total_paid"] += paid
                
                if inv_status not in ["paid", "cancelled"]:
                    summary["total_outstanding"] += (total - paid)
            
            return {
                "invoices": invoices,
                "summary": summary
            }
        
        return result
    
    def record_payment(
        self,
        invoice_id: str,
        amount: float,
        payment_date: Optional[str] = None,
        payment_method: str = "stripe",
        transaction_id: Optional[str] = None,
        notes: Optional[str] = None
    ) -> dict:
        """
        Record a payment for an invoice.
        
        Args:
            invoice_id: Invoice identifier
            amount: Payment amount
            payment_date: Payment date (ISO format), defaults to today
            payment_method: Payment method (stripe, check, wire, cash, other)
            transaction_id: External transaction/payment ID
            notes: Payment notes
        
        Returns:
            Payment record and updated invoice
        """
        invoice_result = self._read_record("invoices", invoice_id)
        if not invoice_result.get("success"):
            return invoice_result
        
        invoice = invoice_result["record"]
        
        if payment_date is None:
            payment_date = date.today().isoformat()
        
        # Generate payment ID
        payment_id = generate_id("payment")
        
        payment_data = {
            "invoice_id": invoice_id,
            "invoice_number": invoice.get("invoice_number"),
            "client_id": invoice.get("client_id"),
            "amount": amount,
            "payment_date": payment_date,
            "payment_method": payment_method,
            "transaction_id": transaction_id,
            "notes": notes
        }
        
        payment_result = self._create_record("payments", payment_id, payment_data)
        
        if payment_result.get("success"):
            # Update invoice
            paid_amount = invoice.get("paid_amount", 0.0) + amount
            total = invoice.get("total", 0.0)
            
            updates = {
                "paid_amount": paid_amount,
                "last_payment_date": payment_date
            }
            
            if paid_amount >= total:
                updates["status"] = "paid"
                updates["paid_date"] = payment_date
            
            self._update_record("invoices", invoice_id, updates)
            
            return {
                "payment_id": payment_id,
                "status": "recorded",
                "payment": payment_result["record"],
                "invoice_status": updates.get("status", invoice.get("status"))
            }
        
        return payment_result
    
    def create_expense(
        self,
        description: str,
        amount: float,
        category: str,
        expense_date: Optional[str] = None,
        vendor: Optional[str] = None,
        receipt_url: Optional[str] = None,
        notes: Optional[str] = None,
        billable_to_client: Optional[str] = None
    ) -> dict:
        """
        Record a business expense.
        
        Args:
            description: Expense description
            amount: Expense amount
            category: IRS expense category
            expense_date: Date of expense (ISO format)
            vendor: Vendor/merchant name
            receipt_url: Link to receipt/documentation
            notes: Additional notes
            billable_to_client: Client ID if billable
        
        Returns:
            Expense record
        """
        # IRS business expense categories
        valid_categories = [
            "advertising",
            "car_and_truck",
            "commissions_and_fees",
            "contract_labor",
            "depletion",
            "depreciation",
            "employee_benefits",
            "insurance",
            "interest",
            "legal_and_professional",
            "office_expense",
            "pension_and_profit_sharing",
            "rent_or_lease",
            "repairs_and_maintenance",
            "supplies",
            "taxes_and_licenses",
            "travel",
            "meals",
            "utilities",
            "wages",
            "other"
        ]
        
        if category not in valid_categories:
            return {
                "error": f"Invalid category. Must be one of: {', '.join(valid_categories)}",
                "valid_categories": valid_categories
            }
        
        if expense_date is None:
            expense_date = date.today().isoformat()
        
        # Generate expense ID
        expense_id = generate_id("expense")
        
        expense_data = {
            "description": description,
            "amount": amount,
            "category": category,
            "expense_date": expense_date,
            "vendor": vendor,
            "receipt_url": receipt_url,
            "notes": notes,
            "billable_to_client": billable_to_client,
            "reimbursed": False,
            "tax_year": int(expense_date[:4])
        }
        
        result = self._create_record("expenses", expense_id, expense_data)
        
        if result.get("success"):
            self.logger.info(f"Recorded expense: {description} - {format_currency(amount)}")
            return {
                "expense_id": expense_id,
                "status": "recorded",
                "expense": result["record"]
            }
        
        return result
    
    def list_expenses(
        self,
        category: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        tax_year: Optional[int] = None
    ) -> dict:
        """
        List expenses with filters.
        
        Args:
            category: Filter by category
            start_date: Filter by start date
            end_date: Filter by end date
            tax_year: Filter by tax year
        
        Returns:
            List of expenses with totals
        """
        def filter_func(expense: dict) -> bool:
            if category and expense.get("category") != category:
                return False
            
            exp_date = expense.get("expense_date")
            if exp_date:
                try:
                    exp_date_obj = date.fromisoformat(exp_date)
                    
                    if start_date:
                        start_obj = date.fromisoformat(start_date)
                        if exp_date_obj < start_obj:
                            return False
                    
                    if end_date:
                        end_obj = date.fromisoformat(end_date)
                        if exp_date_obj > end_obj:
                            return False
                except ValueError:
                    pass
            
            if tax_year and expense.get("tax_year") != tax_year:
                return False
            
            return True
        
        result = self._list_records("expenses", filter_func, sort_key="expense_date", reverse=True)
        
        if result.get("success"):
            expenses = result["records"]
            
            summary = {
                "total_expenses": len(expenses),
                "by_category": {},
                "total_amount": 0.0,
                "billable_expenses": 0.0
            }
            
            for expense in expenses:
                # Category breakdown
                cat = expense.get("category", "unknown")
                summary["by_category"][cat] = summary["by_category"].get(cat, 0.0) + expense.get("amount", 0.0)
                
                # Totals
                summary["total_amount"] += expense.get("amount", 0.0)
                
                if expense.get("billable_to_client"):
                    summary["billable_expenses"] += expense.get("amount", 0.0)
            
            return {
                "expenses": expenses,
                "summary": summary
            }
        
        return result
    
    def get_revenue_report(
        self,
        period: str = "current_month",
        year: Optional[int] = None,
        quarter: Optional[int] = None
    ) -> dict:
        """
        Get revenue report for a time period.
        
        Args:
            period: 'current_month', 'last_month', 'current_quarter', 'last_quarter', 'ytd', 'custom'
            year: Year for custom period
            quarter: Quarter (1-4) for quarterly reports
        
        Returns:
            Revenue breakdown
        """
        today = date.today()
        invoices = self._get_collection("invoices")
        
        # Determine date range
        if period == "current_month":
            start_date = date(today.year, today.month, 1)
            if today.month == 12:
                end_date = date(today.year, 12, 31)
            else:
                end_date = date(today.year, today.month + 1, 1) - timedelta(days=1)
        
        elif period == "last_month":
            if today.month == 1:
                start_date = date(today.year - 1, 12, 1)
                end_date = date(today.year - 1, 12, 31)
            else:
                start_date = date(today.year, today.month - 1, 1)
                end_date = date(today.year, today.month, 1) - timedelta(days=1)
        
        elif period in ["current_quarter", "last_quarter"]:
            current_q, current_year = get_quarter(today)
            
            if period == "current_quarter":
                q, y = current_q, current_year
            else:
                if current_q == 1:
                    q, y = 4, current_year - 1
                else:
                    q, y = current_q - 1, current_year
            
            start_date, end_date = get_quarter_dates(q, y)
        
        elif period == "ytd":
            start_date = date(today.year, 1, 1)
            end_date = today
        
        else:
            # Default to all time
            start_date = date(2000, 1, 1)
            end_date = today
        
        # Calculate revenue
        total_revenue = 0.0
        paid_revenue = 0.0
        outstanding = 0.0
        invoice_count = 0
        
        by_client = {}
        by_month = {}
        
        for invoice in invoices.values():
            issue_date_str = invoice.get("issue_date")
            if not issue_date_str:
                continue
            
            try:
                issue_date_obj = date.fromisoformat(issue_date_str)
            except ValueError:
                continue
            
            if start_date <= issue_date_obj <= end_date:
                total = invoice.get("total", 0.0)
                paid = invoice.get("paid_amount", 0.0)
                status = invoice.get("status")
                
                if status != "cancelled":
                    total_revenue += total
                    paid_revenue += paid
                    
                    if status not in ["paid", "cancelled"]:
                        outstanding += (total - paid)
                    
                    invoice_count += 1
                    
                    # By client
                    client_name = invoice.get("client_name", "Unknown")
                    if client_name not in by_client:
                        by_client[client_name] = 0.0
                    by_client[client_name] += total
                    
                    # By month
                    month_key = issue_date_obj.strftime("%Y-%m")
                    if month_key not in by_month:
                        by_month[month_key] = 0.0
                    by_month[month_key] += total
        
        return {
            "period": period,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "summary": {
                "invoice_count": invoice_count,
                "total_revenue": total_revenue,
                "paid_revenue": paid_revenue,
                "outstanding": outstanding,
                "collection_rate": (paid_revenue / total_revenue * 100) if total_revenue > 0 else 0
            },
            "by_client": by_client,
            "by_month": by_month
        }
    
    def get_profit_margin(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> dict:
        """
        Calculate profit margin for a period.
        
        Args:
            start_date: Start date (ISO format)
            end_date: End date (ISO format)
        
        Returns:
            Profit margin analysis
        """
        if start_date is None:
            start_date = date(date.today().year, 1, 1).isoformat()
        if end_date is None:
            end_date = date.today().isoformat()
        
        # Get revenue
        revenue_report = self.get_revenue_report(period="custom")
        total_revenue = revenue_report["summary"]["paid_revenue"]
        
        # Get expenses
        expense_result = self.list_expenses(start_date=start_date, end_date=end_date)
        total_expenses = expense_result.get("summary", {}).get("total_amount", 0.0)
        
        # Calculate profit
        gross_profit = total_revenue - total_expenses
        profit_margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        return {
            "period": {
                "start_date": start_date,
                "end_date": end_date
            },
            "revenue": total_revenue,
            "expenses": total_expenses,
            "gross_profit": gross_profit,
            "profit_margin_percent": round(profit_margin, 2)
        }
    
    def send_payment_reminder(self, invoice_id: str) -> dict:
        """
        Send payment reminder for an invoice.
        
        Args:
            invoice_id: Invoice identifier
        
        Returns:
            Reminder status
        """
        invoice_result = self._read_record("invoices", invoice_id)
        if not invoice_result.get("success"):
            return invoice_result
        
        invoice = invoice_result["record"]
        
        if invoice.get("status") == "paid":
            return {"error": "Invoice is already paid"}
        
        # Update reminder count
        reminders_sent = invoice.get("reminders_sent", 0) + 1
        
        updates = {
            "reminders_sent": reminders_sent,
            "last_reminder": date.today().isoformat()
        }
        
        self._update_record("invoices", invoice_id, updates)
        
        # Note: Actual email sending would integrate with SMTP here
        self.logger.info(f"Payment reminder sent for invoice {invoice.get('invoice_number')}")
        
        return {
            "invoice_id": invoice_id,
            "status": "reminder_sent",
            "reminders_sent": reminders_sent,
            "message": f"Payment reminder sent (total: {reminders_sent})"
        }
    
    def get_overdue_invoices(self) -> dict:
        """
        Get list of overdue invoices.
        
        Returns:
            Overdue invoices with aging
        """
        result = self.list_invoices(overdue_only=True)
        
        if result.get("success"):
            invoices = result["invoices"]
            
            # Add days overdue
            for invoice in invoices:
                due_date_str = invoice.get("due_date")
                if due_date_str:
                    try:
                        due_date_obj = date.fromisoformat(due_date_str)
                        days_overdue = (date.today() - due_date_obj).days
                        invoice["days_overdue"] = days_overdue
                        
                        # Aging bucket
                        if days_overdue <= 30:
                            invoice["aging_bucket"] = "0-30 days"
                        elif days_overdue <= 60:
                            invoice["aging_bucket"] = "31-60 days"
                        elif days_overdue <= 90:
                            invoice["aging_bucket"] = "61-90 days"
                        else:
                            invoice["aging_bucket"] = "90+ days"
                    except ValueError:
                        invoice["days_overdue"] = None
            
            return {
                "overdue_invoices": invoices,
                "count": len(invoices),
                "total_overdue": result["summary"]["total_outstanding"]
            }
        
        return result


# Standalone functions for MCP tool interface
_server_instance = None

def _get_server() -> BillingServer:
    """Get or create server instance."""
    global _server_instance
    if _server_instance is None:
        _server_instance = BillingServer()
    return _server_instance


def create_invoice(**kwargs) -> dict:
    """Create a new invoice."""
    return _get_server().create_invoice(**kwargs)


def get_invoice(invoice_id: str) -> dict:
    """Get invoice by ID."""
    return _get_server().get_invoice(invoice_id)


def update_invoice_status(**kwargs) -> dict:
    """Update invoice status."""
    return _get_server().update_invoice_status(**kwargs)


def list_invoices(**kwargs) -> dict:
    """List invoices with filters."""
    return _get_server().list_invoices(**kwargs)


def record_payment(**kwargs) -> dict:
    """Record a payment."""
    return _get_server().record_payment(**kwargs)


def create_expense(**kwargs) -> dict:
    """Create an expense record."""
    return _get_server().create_expense(**kwargs)


def list_expenses(**kwargs) -> dict:
    """List expenses with filters."""
    return _get_server().list_expenses(**kwargs)


def get_revenue_report(**kwargs) -> dict:
    """Get revenue report."""
    return _get_server().get_revenue_report(**kwargs)


def get_profit_margin(**kwargs) -> dict:
    """Get profit margin analysis."""
    return _get_server().get_profit_margin(**kwargs)


def send_payment_reminder(invoice_id: str) -> dict:
    """Send payment reminder."""
    return _get_server().send_payment_reminder(invoice_id)


def get_overdue_invoices() -> dict:
    """Get overdue invoices."""
    return _get_server().get_overdue_invoices()


def get_server_info() -> dict:
    """Get server info."""
    return _get_server().get_info()


if __name__ == "__main__":
    server = BillingServer()
    print("Billing Server - Invoicing & Stripe Integration MCP Server")
    print(f"Data file: {server.data_path}")
    print(f"Stripe enabled: {server._stripe_enabled}")
    info = server.get_info()
    print(f"Available tools: {', '.join(info['tools'])}")
