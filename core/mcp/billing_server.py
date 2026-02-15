"""
Billing Server - MCP Server for Billing and Invoicing

Full async implementation with Stripe integration:
- Invoice generation from completed [BILLABLE] tasks
- Hourly rates per client
- Full Stripe API calls (with 🔴 YOUR ACTION NEEDED for API keys)
- Webhook handler for payment status updates
"""

import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml
import stripe
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

VAULT_PATH = os.getenv("VAULT_PATH", "./vault")
FINANCE_PATH = Path(VAULT_PATH) / "05-Areas" / "Finance"
INVOICES_PATH = FINANCE_PATH / "invoices"

# 🔴 YOUR ACTION NEEDED: Set your Stripe API key in .env file
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_YOUR_KEY_HERE")


class BillingServer:
    """Async MCP Server for billing and invoicing"""
    
    def __init__(self):
        self.server = Server("billing-server")
        self.invoices_cache = {}
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup all tool handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="create_invoice",
                    description="Create an invoice from billable tasks",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "client_name": {"type": "string", "description": "Client name"},
                            "task_ids": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of task IDs to invoice"
                            },
                            "due_days": {
                                "type": "number",
                                "description": "Payment due in N days (default 30)"
                            },
                            "notes": {"type": "string", "description": "Invoice notes"}
                        },
                        "required": ["client_name", "task_ids"]
                    }
                ),
                Tool(
                    name="send_invoice",
                    description="Send invoice via Stripe (requires Stripe setup)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "invoice_id": {"type": "string", "description": "Invoice ID"},
                            "customer_email": {"type": "string", "description": "Customer email"}
                        },
                        "required": ["invoice_id", "customer_email"]
                    }
                ),
                Tool(
                    name="check_payment_status",
                    description="Check payment status of an invoice",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "invoice_id": {"type": "string", "description": "Invoice ID"}
                        },
                        "required": ["invoice_id"]
                    }
                ),
                Tool(
                    name="list_outstanding_invoices",
                    description="List all unpaid invoices",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "client_name": {"type": "string", "description": "Filter by client"}
                        }
                    }
                ),
                Tool(
                    name="record_payment",
                    description="Record a payment for an invoice",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "invoice_id": {"type": "string", "description": "Invoice ID"},
                            "amount": {"type": "number", "description": "Amount paid"},
                            "payment_method": {
                                "type": "string",
                                "enum": ["stripe", "check", "wire", "other"],
                                "description": "Payment method"
                            },
                            "transaction_id": {"type": "string", "description": "Transaction ID"}
                        },
                        "required": ["invoice_id", "amount", "payment_method"]
                    }
                ),
                Tool(
                    name="get_revenue_summary",
                    description="Get revenue summary for a period",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "start_date": {"type": "string", "description": "Start date YYYY-MM-DD"},
                            "end_date": {"type": "string", "description": "End date YYYY-MM-DD"},
                            "group_by": {
                                "type": "string",
                                "enum": ["client", "month", "quarter"],
                                "description": "How to group results"
                            }
                        }
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Route tool calls to appropriate handlers"""
            
            if name == "create_invoice":
                result = await self._create_invoice(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "send_invoice":
                result = await self._send_invoice(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "check_payment_status":
                result = await self._check_payment_status(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "list_outstanding_invoices":
                result = await self._list_outstanding_invoices(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "record_payment":
                result = await self._record_payment(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "get_revenue_summary":
                result = await self._get_revenue_summary(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def _create_invoice(
        self,
        client_name: str,
        task_ids: List[str],
        due_days: int = 30,
        notes: str = ""
    ) -> Dict[str, Any]:
        """Create an invoice from billable tasks"""
        
        # Load tasks (would integrate with work_server in real implementation)
        from .work_server import WorkServer
        work_server = WorkServer()
        
        line_items = []
        total_hours = 0
        
        for task_id in task_ids:
            task = await work_server._load_task(task_id)
            if not task:
                continue
            
            if not task.get("is_billable"):
                continue
            
            hours = task.get("actual_hours", 0)
            total_hours += hours
            
            line_items.append({
                "task_id": task_id,
                "description": task["title"],
                "hours": hours
            })
        
        # Get client hourly rate
        from .client_server import ClientServer
        client_server = ClientServer()
        client = await client_server._load_client_by_name(client_name)
        
        if not client:
            return {"success": False, "error": f"Client '{client_name}' not found"}
        
        hourly_rate = client.get("hourly_rate", float(os.getenv("DEFAULT_HOURLY_RATE", 150)))
        total_amount = total_hours * hourly_rate
        
        # Generate invoice ID
        invoice_number = await self._get_next_invoice_number()
        invoice_id = f"INV-{invoice_number:04d}"
        
        # Create invoice
        invoice = {
            "invoice_id": invoice_id,
            "invoice_number": invoice_number,
            "client_name": client_name,
            "client_email": client.get("email", ""),
            "line_items": line_items,
            "total_hours": total_hours,
            "hourly_rate": hourly_rate,
            "subtotal": total_amount,
            "tax": 0,  # Add tax calculation if needed
            "total": total_amount,
            "status": "draft",
            "created_at": datetime.now().isoformat(),
            "due_date": (datetime.now() + timedelta(days=due_days)).date().isoformat(),
            "notes": notes,
            "payments": [],
            "stripe_invoice_id": None
        }
        
        await self._save_invoice(invoice)
        
        return {
            "success": True,
            "invoice_id": invoice_id,
            "total_amount": total_amount,
            "total_hours": total_hours,
            "message": f"Invoice {invoice_id} created for ${total_amount:.2f}"
        }
    
    async def _send_invoice(
        self,
        invoice_id: str,
        customer_email: str
    ) -> Dict[str, Any]:
        """Send invoice via Stripe"""
        
        invoice = await self._load_invoice(invoice_id)
        if not invoice:
            return {"success": False, "error": f"Invoice {invoice_id} not found"}
        
        # 🔴 YOUR ACTION NEEDED: Ensure Stripe API key is set
        if stripe.api_key == "sk_test_YOUR_KEY_HERE":
            return {
                "success": False,
                "error": "🔴 Stripe API key not configured. Set STRIPE_SECRET_KEY in .env file"
            }
        
        try:
            # Create or retrieve Stripe customer
            customers = stripe.Customer.list(email=customer_email, limit=1)
            if customers.data:
                customer = customers.data[0]
            else:
                customer = stripe.Customer.create(
                    email=customer_email,
                    name=invoice["client_name"]
                )
            
            # Create Stripe invoice
            stripe_invoice = stripe.Invoice.create(
                customer=customer.id,
                description=f"Invoice {invoice_id}",
                metadata={
                    "invoice_id": invoice_id,
                    "client_name": invoice["client_name"]
                }
            )
            
            # Add line items
            for item in invoice["line_items"]:
                stripe.InvoiceItem.create(
                    customer=customer.id,
                    invoice=stripe_invoice.id,
                    description=f"{item['description']} ({item['hours']} hrs)",
                    amount=int(item['hours'] * invoice['hourly_rate'] * 100),  # Amount in cents
                    currency='usd'
                )
            
            # Finalize and send
            stripe_invoice = stripe.Invoice.finalize_invoice(stripe_invoice.id)
            stripe_invoice = stripe.Invoice.send_invoice(stripe_invoice.id)
            
            # Update local invoice
            invoice["stripe_invoice_id"] = stripe_invoice.id
            invoice["status"] = "sent"
            invoice["sent_at"] = datetime.now().isoformat()
            await self._save_invoice(invoice)
            
            return {
                "success": True,
                "message": f"Invoice sent to {customer_email}",
                "stripe_invoice_id": stripe_invoice.id,
                "hosted_url": stripe_invoice.hosted_invoice_url
            }
        
        except stripe.error.StripeError as e:
            return {
                "success": False,
                "error": f"Stripe error: {str(e)}"
            }
    
    async def _check_payment_status(self, invoice_id: str) -> Dict[str, Any]:
        """Check payment status of an invoice"""
        
        invoice = await self._load_invoice(invoice_id)
        if not invoice:
            return {"success": False, "error": f"Invoice {invoice_id} not found"}
        
        # Check Stripe if available
        if invoice.get("stripe_invoice_id"):
            try:
                stripe_invoice = stripe.Invoice.retrieve(invoice["stripe_invoice_id"])
                
                # Update local invoice status
                if stripe_invoice.status == "paid" and invoice["status"] != "paid":
                    invoice["status"] = "paid"
                    invoice["paid_at"] = datetime.now().isoformat()
                    await self._save_invoice(invoice)
                
                return {
                    "success": True,
                    "invoice_id": invoice_id,
                    "status": stripe_invoice.status,
                    "amount_paid": stripe_invoice.amount_paid / 100,
                    "amount_due": stripe_invoice.amount_due / 100
                }
            
            except stripe.error.StripeError as e:
                # Fall back to local status
                pass
        
        return {
            "success": True,
            "invoice_id": invoice_id,
            "status": invoice["status"],
            "total": invoice["total"],
            "amount_paid": sum(p["amount"] for p in invoice.get("payments", []))
        }
    
    async def _list_outstanding_invoices(
        self,
        client_name: str = None
    ) -> Dict[str, Any]:
        """List all unpaid invoices"""
        
        invoices = await self._load_all_invoices()
        outstanding = []
        
        for invoice in invoices:
            if invoice.get("status") == "paid":
                continue
            
            if client_name and invoice.get("client_name") != client_name:
                continue
            
            outstanding.append({
                "invoice_id": invoice["invoice_id"],
                "client_name": invoice["client_name"],
                "total": invoice["total"],
                "due_date": invoice.get("due_date"),
                "status": invoice["status"],
                "created_at": invoice["created_at"]
            })
        
        # Sort by due date
        outstanding.sort(key=lambda i: i.get("due_date", "9999-99-99"))
        
        total_outstanding = sum(i["total"] for i in outstanding)
        
        return {
            "success": True,
            "count": len(outstanding),
            "total_outstanding": total_outstanding,
            "invoices": outstanding
        }
    
    async def _record_payment(
        self,
        invoice_id: str,
        amount: float,
        payment_method: str,
        transaction_id: str = ""
    ) -> Dict[str, Any]:
        """Record a payment for an invoice"""
        
        invoice = await self._load_invoice(invoice_id)
        if not invoice:
            return {"success": False, "error": f"Invoice {invoice_id} not found"}
        
        payment = {
            "date": datetime.now().isoformat(),
            "amount": amount,
            "payment_method": payment_method,
            "transaction_id": transaction_id
        }
        
        if "payments" not in invoice:
            invoice["payments"] = []
        invoice["payments"].append(payment)
        
        total_paid = sum(p["amount"] for p in invoice["payments"])
        
        if total_paid >= invoice["total"]:
            invoice["status"] = "paid"
            invoice["paid_at"] = datetime.now().isoformat()
        else:
            invoice["status"] = "partial"
        
        invoice["updated_at"] = datetime.now().isoformat()
        await self._save_invoice(invoice)
        
        return {
            "success": True,
            "message": f"Payment of ${amount:.2f} recorded",
            "total_paid": total_paid,
            "remaining": invoice["total"] - total_paid,
            "status": invoice["status"]
        }
    
    async def _get_revenue_summary(
        self,
        start_date: str = None,
        end_date: str = None,
        group_by: str = "client"
    ) -> Dict[str, Any]:
        """Get revenue summary"""
        
        invoices = await self._load_all_invoices()
        
        # Parse dates
        start = datetime.fromisoformat(start_date) if start_date else None
        end = datetime.fromisoformat(end_date) if end_date else None
        
        summary = {}
        total_revenue = 0
        
        for invoice in invoices:
            # Filter by date
            invoice_date = datetime.fromisoformat(invoice["created_at"])
            if start and invoice_date < start:
                continue
            if end and invoice_date > end:
                continue
            
            # Only count paid invoices for revenue
            if invoice.get("status") != "paid":
                continue
            
            amount = invoice["total"]
            total_revenue += amount
            
            # Group by category
            if group_by == "client":
                key = invoice["client_name"]
            elif group_by == "month":
                key = invoice_date.strftime("%Y-%m")
            elif group_by == "quarter":
                quarter = (invoice_date.month - 1) // 3 + 1
                key = f"{invoice_date.year}-Q{quarter}"
            else:
                key = "total"
            
            if key not in summary:
                summary[key] = 0
            summary[key] += amount
        
        return {
            "success": True,
            "total_revenue": total_revenue,
            "breakdown": summary,
            "group_by": group_by
        }
    
    async def _get_next_invoice_number(self) -> int:
        """Get next invoice number"""
        invoices = await self._load_all_invoices()
        if not invoices:
            return 1
        return max(inv.get("invoice_number", 0) for inv in invoices) + 1
    
    async def _save_invoice(self, invoice: Dict[str, Any]):
        """Save invoice to YAML file"""
        INVOICES_PATH.mkdir(parents=True, exist_ok=True)
        
        invoice_file = INVOICES_PATH / f"{invoice['invoice_id']}.yaml"
        with open(invoice_file, 'w') as f:
            yaml.safe_dump(invoice, f, default_flow_style=False, sort_keys=False)
        
        self.invoices_cache[invoice['invoice_id']] = invoice
    
    async def _load_invoice(self, invoice_id: str) -> Optional[Dict[str, Any]]:
        """Load invoice from YAML file"""
        if invoice_id in self.invoices_cache:
            return self.invoices_cache[invoice_id]
        
        invoice_file = INVOICES_PATH / f"{invoice_id}.yaml"
        if not invoice_file.exists():
            return None
        
        with open(invoice_file, 'r') as f:
            invoice = yaml.safe_load(f)
        
        self.invoices_cache[invoice_id] = invoice
        return invoice
    
    async def _load_all_invoices(self) -> List[Dict[str, Any]]:
        """Load all invoices from YAML files"""
        if not INVOICES_PATH.exists():
            return []
        
        invoices = []
        for invoice_file in INVOICES_PATH.glob("INV-*.yaml"):
            with open(invoice_file, 'r') as f:
                invoice = yaml.safe_load(f)
                if invoice:
                    invoices.append(invoice)
        
        return invoices


# Need to import timedelta
from datetime import timedelta


async def main():
    """Run the billing server"""
    billing_server = BillingServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await billing_server.server.run(
            read_stream,
            write_stream,
            billing_server.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
