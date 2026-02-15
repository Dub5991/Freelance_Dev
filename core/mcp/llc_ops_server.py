"""
LLC Operations Server - MCP Server for LLC Financial Operations

Full async implementation for:
- Revenue tracking (fed from billing server)
- Expense logging with categories
- Quarterly tax estimates (Q1 Apr 15, Q2 Jun 15, Q3 Sep 15, Q4 Jan 15)
- Profit/loss calculations
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
FINANCE_PATH = Path(VAULT_PATH) / "05-Areas" / "Finance"
EXPENSES_PATH = FINANCE_PATH / "expenses"
TAX_PATH = FINANCE_PATH / "tax"

QUARTERLY_TAX_RATE = float(os.getenv("QUARTERLY_TAX_RATE", 0.25))

# Quarterly tax deadlines
TAX_DEADLINES = {
    "Q1": (4, 15),  # April 15
    "Q2": (6, 15),  # June 15
    "Q3": (9, 15),  # September 15
    "Q4": (1, 15),  # January 15 (next year)
}


class LLCOpsServer:
    """Async MCP Server for LLC operations and finances"""
    
    def __init__(self):
        self.server = Server("llc-ops-server")
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup all tool handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="get_dashboard",
                    description="Get financial dashboard with key metrics",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "year": {"type": "number", "description": "Year (default current)"},
                            "quarter": {"type": "number", "description": "Quarter 1-4 (optional)"}
                        }
                    }
                ),
                Tool(
                    name="log_expense",
                    description="Log a business expense",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "amount": {"type": "number", "description": "Expense amount"},
                            "category": {
                                "type": "string",
                                "enum": [
                                    "Software", "Hardware", "Office", "Travel",
                                    "Education", "Marketing", "Legal", "Accounting",
                                    "Insurance", "Meals", "Other"
                                ],
                                "description": "Expense category"
                            },
                            "description": {"type": "string", "description": "Expense description"},
                            "date": {"type": "string", "description": "Expense date YYYY-MM-DD"},
                            "vendor": {"type": "string", "description": "Vendor/payee name"}
                        },
                        "required": ["amount", "category", "description"]
                    }
                ),
                Tool(
                    name="get_tax_estimate",
                    description="Get quarterly tax estimate",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "year": {"type": "number", "description": "Tax year"},
                            "quarter": {
                                "type": "number",
                                "minimum": 1,
                                "maximum": 4,
                                "description": "Quarter number 1-4"
                            }
                        },
                        "required": ["year", "quarter"]
                    }
                ),
                Tool(
                    name="get_profit_loss",
                    description="Get profit and loss statement",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "start_date": {"type": "string", "description": "Start date YYYY-MM-DD"},
                            "end_date": {"type": "string", "description": "End date YYYY-MM-DD"}
                        },
                        "required": ["start_date", "end_date"]
                    }
                ),
                Tool(
                    name="get_revenue_by_client",
                    description="Get revenue breakdown by client",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "year": {"type": "number", "description": "Year (default current)"}
                        }
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Route tool calls to appropriate handlers"""
            
            if name == "get_dashboard":
                result = await self._get_dashboard(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "log_expense":
                result = await self._log_expense(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "get_tax_estimate":
                result = await self._get_tax_estimate(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "get_profit_loss":
                result = await self._get_profit_loss(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            elif name == "get_revenue_by_client":
                result = await self._get_revenue_by_client(**arguments)
                return [TextContent(type="text", text=str(result))]
            
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def _get_dashboard(
        self,
        year: int = None,
        quarter: int = None
    ) -> Dict[str, Any]:
        """Get financial dashboard"""
        
        year = year or datetime.now().year
        
        # Get revenue from billing server
        from .billing_server import BillingServer
        billing_server = BillingServer()
        
        if quarter:
            start_month = (quarter - 1) * 3 + 1
            end_month = start_month + 2
            start_date = f"{year}-{start_month:02d}-01"
            
            # Calculate last day of end month
            if end_month == 12:
                end_date = f"{year}-12-31"
            else:
                from calendar import monthrange
                _, last_day = monthrange(year, end_month)
                end_date = f"{year}-{end_month:02d}-{last_day:02d}"
        else:
            start_date = f"{year}-01-01"
            end_date = f"{year}-12-31"
        
        revenue_result = await billing_server._get_revenue_summary(
            start_date=start_date,
            end_date=end_date,
            group_by="client"
        )
        
        total_revenue = revenue_result.get("total_revenue", 0)
        
        # Get expenses
        expenses = await self._get_expenses(start_date, end_date)
        total_expenses = sum(e["amount"] for e in expenses)
        
        # Calculate profit
        profit = total_revenue - total_expenses
        profit_margin = (profit / total_revenue * 100) if total_revenue > 0 else 0
        
        # Get outstanding invoices
        outstanding_result = await billing_server._list_outstanding_invoices()
        outstanding_amount = outstanding_result.get("total_outstanding", 0)
        
        # Tax estimate
        estimated_tax = profit * QUARTERLY_TAX_RATE
        
        return {
            "success": True,
            "period": f"Q{quarter} {year}" if quarter else f"{year}",
            "revenue": total_revenue,
            "expenses": total_expenses,
            "profit": profit,
            "profit_margin": round(profit_margin, 2),
            "outstanding_invoices": outstanding_amount,
            "estimated_tax": estimated_tax,
            "net_after_tax": profit - estimated_tax
        }
    
    async def _log_expense(
        self,
        amount: float,
        category: str,
        description: str,
        date: str = None,
        vendor: str = ""
    ) -> Dict[str, Any]:
        """Log a business expense"""
        
        EXPENSES_PATH.mkdir(parents=True, exist_ok=True)
        
        # Generate expense ID
        expense_date = date or datetime.now().date().isoformat()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        expense_id = f"EXP-{timestamp}"
        
        expense = {
            "expense_id": expense_id,
            "amount": amount,
            "category": category,
            "description": description,
            "vendor": vendor,
            "date": expense_date,
            "created_at": datetime.now().isoformat()
        }
        
        # Save to YAML
        expense_file = EXPENSES_PATH / f"{expense_id}.yaml"
        with open(expense_file, 'w') as f:
            yaml.safe_dump(expense, f, default_flow_style=False, sort_keys=False)
        
        return {
            "success": True,
            "expense_id": expense_id,
            "message": f"Expense logged: ${amount:.2f} - {description}"
        }
    
    async def _get_tax_estimate(self, year: int, quarter: int) -> Dict[str, Any]:
        """Get quarterly tax estimate"""
        
        # Calculate quarter date range
        start_month = (quarter - 1) * 3 + 1
        end_month = start_month + 2
        
        start_date = f"{year}-{start_month:02d}-01"
        
        # Calculate last day of end month
        if end_month == 12:
            end_date = f"{year}-12-31"
        else:
            from calendar import monthrange
            _, last_day = monthrange(year, end_month)
            end_date = f"{year}-{end_month:02d}-{last_day:02d}"
        
        # Get P&L for quarter
        pl_result = await self._get_profit_loss(start_date, end_date)
        
        profit = pl_result.get("net_income", 0)
        estimated_tax = profit * QUARTERLY_TAX_RATE
        
        # Calculate deadline
        deadline_month, deadline_day = TAX_DEADLINES[f"Q{quarter}"]
        deadline_year = year if quarter != 4 else year + 1
        deadline = date(deadline_year, deadline_month, deadline_day)
        days_until = (deadline - date.today()).days
        
        return {
            "success": True,
            "year": year,
            "quarter": quarter,
            "profit": profit,
            "tax_rate": QUARTERLY_TAX_RATE,
            "estimated_tax": estimated_tax,
            "deadline": deadline.isoformat(),
            "days_until_deadline": days_until,
            "is_overdue": days_until < 0
        }
    
    async def _get_profit_loss(
        self,
        start_date: str,
        end_date: str
    ) -> Dict[str, Any]:
        """Get profit and loss statement"""
        
        # Get revenue
        from .billing_server import BillingServer
        billing_server = BillingServer()
        
        revenue_result = await billing_server._get_revenue_summary(
            start_date=start_date,
            end_date=end_date,
            group_by="client"
        )
        
        total_revenue = revenue_result.get("total_revenue", 0)
        
        # Get expenses
        expenses = await self._get_expenses(start_date, end_date)
        
        # Group expenses by category
        expenses_by_category = {}
        for expense in expenses:
            category = expense["category"]
            if category not in expenses_by_category:
                expenses_by_category[category] = 0
            expenses_by_category[category] += expense["amount"]
        
        total_expenses = sum(expenses_by_category.values())
        net_income = total_revenue - total_expenses
        
        return {
            "success": True,
            "period": f"{start_date} to {end_date}",
            "revenue": total_revenue,
            "expenses_by_category": expenses_by_category,
            "total_expenses": total_expenses,
            "net_income": net_income,
            "margin": round((net_income / total_revenue * 100), 2) if total_revenue > 0 else 0
        }
    
    async def _get_revenue_by_client(self, year: int = None) -> Dict[str, Any]:
        """Get revenue breakdown by client"""
        
        year = year or datetime.now().year
        
        from .billing_server import BillingServer
        billing_server = BillingServer()
        
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        
        result = await billing_server._get_revenue_summary(
            start_date=start_date,
            end_date=end_date,
            group_by="client"
        )
        
        # Sort by revenue descending
        client_revenue = [
            {"client": client, "revenue": revenue}
            for client, revenue in result.get("breakdown", {}).items()
        ]
        client_revenue.sort(key=lambda x: x["revenue"], reverse=True)
        
        # Calculate percentages
        total = result.get("total_revenue", 0)
        for item in client_revenue:
            item["percentage"] = round((item["revenue"] / total * 100), 2) if total > 0 else 0
        
        return {
            "success": True,
            "year": year,
            "total_revenue": total,
            "clients": client_revenue
        }
    
    async def _get_expenses(
        self,
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]]:
        """Get expenses for date range"""
        
        if not EXPENSES_PATH.exists():
            return []
        
        start = datetime.fromisoformat(start_date).date()
        end = datetime.fromisoformat(end_date).date()
        
        expenses = []
        for expense_file in EXPENSES_PATH.glob("EXP-*.yaml"):
            with open(expense_file, 'r') as f:
                expense = yaml.safe_load(f)
                if not expense:
                    continue
                
                expense_date = datetime.fromisoformat(expense["date"]).date()
                if start <= expense_date <= end:
                    expenses.append(expense)
        
        return expenses


async def main():
    """Run the LLC ops server"""
    llc_ops_server = LLCOpsServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await llc_ops_server.server.run(
            read_stream,
            write_stream,
            llc_ops_server.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
