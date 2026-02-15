"""
LLC Operations Server - Business Entity and Compliance Management MCP Server

Features:
- Business entity management (EIN, state registration)
- Tax deadline tracking and reminders
- Quarterly estimated tax calculations
- Business expense categorization
- Annual compliance checklist
- Document management
"""

from datetime import datetime, date, timedelta
from typing import Optional, List
from ..config import Config
from ..utils import (
    generate_id,
    format_date,
    get_quarter,
    get_quarter_dates
)
from .base_server import BaseMCPServer


class LLCOpsServer(BaseMCPServer):
    """LLC operations and compliance management server."""
    
    def __init__(self):
        super().__init__("llc_ops")
        
        # Initialize collections
        if "entity_info" not in self._data:
            self._data["entity_info"] = {
                "llc_name": Config.LLC_NAME,
                "ein": Config.LLC_EIN,
                "state": Config.LLC_STATE,
                "address": Config.LLC_ADDRESS,
                "formation_date": None,
                "fiscal_year_end": "12-31",
                "tax_classification": "disregarded_entity"
            }
        
        if "tax_deadlines" not in self._data:
            self._data["tax_deadlines"] = {}
        
        if "compliance_items" not in self._data:
            self._data["compliance_items"] = {}
        
        if "documents" not in self._data:
            self._data["documents"] = {}
        
        # Initialize tax deadlines for current year
        self._initialize_tax_deadlines()
    
    def get_info(self) -> dict:
        """Return server metadata."""
        return {
            "name": "llc-ops-server",
            "version": "0.1.0",
            "description": "LLC operations and compliance MCP server",
            "tools": [
                "get_entity_info",
                "update_entity_info",
                "get_tax_deadlines",
                "calculate_quarterly_estimate",
                "add_compliance_item",
                "get_compliance_checklist",
                "complete_compliance_item",
                "upload_document",
                "list_documents",
                "get_tax_summary"
            ]
        }
    
    def _initialize_tax_deadlines(self) -> None:
        """Initialize standard tax deadlines for the current year."""
        year = Config.TAX_YEAR
        deadlines = self._get_collection("tax_deadlines")
        
        # Only initialize if empty
        if not deadlines:
            standard_deadlines = [
                {
                    "name": "Q1 Estimated Tax",
                    "due_date": f"{year}-04-15",
                    "type": "quarterly_estimate",
                    "quarter": 1
                },
                {
                    "name": "Q2 Estimated Tax",
                    "due_date": f"{year}-06-15",
                    "type": "quarterly_estimate",
                    "quarter": 2
                },
                {
                    "name": "Q3 Estimated Tax",
                    "due_date": f"{year}-09-15",
                    "type": "quarterly_estimate",
                    "quarter": 3
                },
                {
                    "name": "Q4 Estimated Tax",
                    "due_date": f"{year + 1}-01-15",
                    "type": "quarterly_estimate",
                    "quarter": 4
                },
                {
                    "name": "Annual Tax Return",
                    "due_date": f"{year + 1}-04-15",
                    "type": "annual_return",
                    "description": "File Schedule C with Form 1040"
                }
            ]
            
            for deadline_data in standard_deadlines:
                deadline_id = generate_id("deadline", date_part=False)
                deadline_data.update({
                    "year": year,
                    "status": "pending",
                    "completed_date": None,
                    "notes": ""
                })
                deadlines[deadline_id] = deadline_data
            
            self._set_collection("tax_deadlines", deadlines)
            self._save_data()
    
    def get_entity_info(self) -> dict:
        """
        Get LLC entity information.
        
        Returns:
            Entity details
        """
        entity_info = self._data.get("entity_info", {})
        return {
            "entity": entity_info
        }
    
    def update_entity_info(self, **updates) -> dict:
        """
        Update LLC entity information.
        
        Args:
            **updates: Fields to update
        
        Returns:
            Updated entity info
        """
        entity_info = self._data.get("entity_info", {})
        entity_info.update(updates)
        entity_info["updated_at"] = datetime.now().isoformat()
        
        self._data["entity_info"] = entity_info
        self._save_data()
        
        return {
            "status": "updated",
            "entity": entity_info
        }
    
    def get_tax_deadlines(
        self,
        year: Optional[int] = None,
        upcoming_only: bool = True
    ) -> dict:
        """
        Get tax deadlines.
        
        Args:
            year: Tax year (defaults to current)
            upcoming_only: Show only upcoming deadlines
        
        Returns:
            List of tax deadlines
        """
        if year is None:
            year = Config.TAX_YEAR
        
        deadlines = self._get_collection("tax_deadlines")
        
        result = []
        for deadline_id, deadline in deadlines.items():
            if deadline.get("year") != year:
                continue
            
            if upcoming_only and deadline.get("status") == "completed":
                continue
            
            # Calculate days until due
            due_date_str = deadline.get("due_date")
            if due_date_str:
                try:
                    due_date_obj = date.fromisoformat(due_date_str)
                    days_until = (due_date_obj - date.today()).days
                    deadline["days_until_due"] = days_until
                    
                    if days_until < 0:
                        deadline["is_overdue"] = True
                    else:
                        deadline["is_overdue"] = False
                except ValueError:
                    pass
            
            deadline["id"] = deadline_id
            result.append(deadline)
        
        # Sort by due date
        result.sort(key=lambda d: d.get("due_date", ""))
        
        return {
            "year": year,
            "deadlines": result,
            "count": len(result)
        }
    
    def calculate_quarterly_estimate(
        self,
        quarter: int,
        year: Optional[int] = None,
        projected_revenue: Optional[float] = None,
        projected_expenses: Optional[float] = None
    ) -> dict:
        """
        Calculate quarterly estimated tax payment.
        
        Args:
            quarter: Quarter number (1-4)
            year: Tax year
            projected_revenue: Projected revenue for the quarter
            projected_expenses: Projected expenses for the quarter
        
        Returns:
            Estimated tax calculation
        """
        if not 1 <= quarter <= 4:
            return {"error": "Quarter must be between 1 and 4"}
        
        if year is None:
            year = Config.TAX_YEAR
        
        # Get actual revenue and expenses from billing server if not provided
        if projected_revenue is None or projected_expenses is None:
            # Default to zero if billing data not available
            projected_revenue = projected_revenue or 0.0
            projected_expenses = projected_expenses or 0.0
        
        # Calculate net income
        net_income = projected_revenue - projected_expenses
        
        # Calculate estimated tax (simplified calculation)
        # Self-employment tax (15.3% on 92.35% of net income)
        se_tax_base = net_income * 0.9235
        se_tax = se_tax_base * 0.153
        
        # Income tax (using configured rate)
        income_tax = net_income * Config.QUARTERLY_TAX_RATE
        
        # Total quarterly payment
        total_estimate = (se_tax + income_tax) / 4
        
        # Get deadline
        deadlines = self.get_tax_deadlines(year=year)
        deadline_info = None
        for dl in deadlines.get("deadlines", []):
            if dl.get("quarter") == quarter:
                deadline_info = dl
                break
        
        return {
            "quarter": quarter,
            "year": year,
            "calculation": {
                "projected_revenue": projected_revenue,
                "projected_expenses": projected_expenses,
                "net_income": net_income,
                "self_employment_tax_annual": se_tax,
                "income_tax_annual": income_tax,
                "total_annual_tax": se_tax + income_tax,
                "quarterly_payment": total_estimate
            },
            "deadline": deadline_info,
            "notes": [
                "This is a simplified calculation",
                "Consult with a tax professional for accurate estimates",
                "Consider state tax obligations separately"
            ]
        }
    
    def add_compliance_item(
        self,
        title: str,
        description: str,
        due_date: Optional[str] = None,
        category: str = "general",
        priority: str = "medium",
        recurring: bool = False,
        recurrence_period: Optional[str] = None
    ) -> dict:
        """
        Add a compliance item to track.
        
        Args:
            title: Item title
            description: Detailed description
            due_date: Due date (ISO format)
            category: Category (annual_filing, state_requirement, federal_requirement, general)
            priority: Priority (high, medium, low)
            recurring: Whether this is a recurring item
            recurrence_period: If recurring, the period (annual, quarterly, monthly)
        
        Returns:
            Compliance item record
        """
        item_id = generate_id("compliance")
        
        item_data = {
            "title": title,
            "description": description,
            "due_date": due_date,
            "category": category,
            "priority": priority,
            "status": "pending",
            "completed_date": None,
            "recurring": recurring,
            "recurrence_period": recurrence_period,
            "notes": ""
        }
        
        result = self._create_record("compliance_items", item_id, item_data)
        
        if result.get("success"):
            return {
                "item_id": item_id,
                "status": "created",
                "item": result["record"]
            }
        
        return result
    
    def get_compliance_checklist(
        self,
        category: Optional[str] = None,
        status: Optional[str] = None
    ) -> dict:
        """
        Get compliance checklist.
        
        Args:
            category: Filter by category
            status: Filter by status (pending, completed, overdue)
        
        Returns:
            Compliance items
        """
        def filter_func(item: dict) -> bool:
            if category and item.get("category") != category:
                return False
            
            item_status = item.get("status")
            
            # Determine if overdue
            if item_status == "pending":
                due_date_str = item.get("due_date")
                if due_date_str:
                    try:
                        due_date_obj = date.fromisoformat(due_date_str)
                        if due_date_obj < date.today():
                            item_status = "overdue"
                    except ValueError:
                        pass
            
            if status and item_status != status:
                return False
            
            return True
        
        result = self._list_records("compliance_items", filter_func, sort_key="due_date")
        
        if result.get("success"):
            items = result["records"]
            
            summary = {
                "total": len(items),
                "by_status": {},
                "by_category": {},
                "by_priority": {}
            }
            
            for item in items:
                # Add days until due
                due_date_str = item.get("due_date")
                if due_date_str:
                    try:
                        due_date_obj = date.fromisoformat(due_date_str)
                        days_until = (due_date_obj - date.today()).days
                        item["days_until_due"] = days_until
                    except ValueError:
                        pass
                
                # Count by status
                item_status = item.get("status", "unknown")
                summary["by_status"][item_status] = summary["by_status"].get(item_status, 0) + 1
                
                # Count by category
                cat = item.get("category", "unknown")
                summary["by_category"][cat] = summary["by_category"].get(cat, 0) + 1
                
                # Count by priority
                pri = item.get("priority", "unknown")
                summary["by_priority"][pri] = summary["by_priority"].get(pri, 0) + 1
            
            return {
                "items": items,
                "summary": summary
            }
        
        return result
    
    def complete_compliance_item(
        self,
        item_id: str,
        notes: Optional[str] = None
    ) -> dict:
        """
        Mark a compliance item as completed.
        
        Args:
            item_id: Item identifier
            notes: Completion notes
        
        Returns:
            Updated item
        """
        updates = {
            "status": "completed",
            "completed_date": date.today().isoformat()
        }
        
        if notes:
            updates["notes"] = notes
        
        result = self._update_record("compliance_items", item_id, updates)
        
        if result.get("success"):
            item = result["record"]
            
            # If recurring, create next instance
            if item.get("recurring") and item.get("recurrence_period"):
                self._create_recurring_item(item)
            
            return {
                "item_id": item_id,
                "status": "completed",
                "item": result["record"]
            }
        
        return result
    
    def _create_recurring_item(self, original_item: dict) -> None:
        """Create next instance of a recurring compliance item."""
        period = original_item.get("recurrence_period")
        due_date_str = original_item.get("due_date")
        
        if not due_date_str:
            return
        
        try:
            due_date_obj = date.fromisoformat(due_date_str)
            
            # Calculate next due date
            if period == "annual":
                next_due = date(due_date_obj.year + 1, due_date_obj.month, due_date_obj.day)
            elif period == "quarterly":
                # Add 3 months
                next_month = due_date_obj.month + 3
                next_year = due_date_obj.year
                if next_month > 12:
                    next_month -= 12
                    next_year += 1
                next_due = date(next_year, next_month, due_date_obj.day)
            elif period == "monthly":
                # Add 1 month
                next_month = due_date_obj.month + 1
                next_year = due_date_obj.year
                if next_month > 12:
                    next_month = 1
                    next_year += 1
                next_due = date(next_year, next_month, due_date_obj.day)
            else:
                return
            
            # Create new item
            self.add_compliance_item(
                title=original_item.get("title"),
                description=original_item.get("description"),
                due_date=next_due.isoformat(),
                category=original_item.get("category"),
                priority=original_item.get("priority"),
                recurring=True,
                recurrence_period=period
            )
        
        except (ValueError, TypeError):
            pass
    
    def upload_document(
        self,
        document_type: str,
        filename: str,
        file_path: str,
        description: Optional[str] = None,
        year: Optional[int] = None,
        tags: Optional[List[str]] = None
    ) -> dict:
        """
        Register a business document.
        
        Args:
            document_type: Type (contract, w9, 1099, tax_return, articles, operating_agreement, other)
            filename: Document filename
            file_path: Path or URL to document
            description: Document description
            year: Associated tax year
            tags: Document tags
        
        Returns:
            Document record
        """
        doc_id = generate_id("doc")
        
        doc_data = {
            "type": document_type,
            "filename": filename,
            "file_path": file_path,
            "description": description,
            "year": year,
            "tags": tags or [],
            "upload_date": date.today().isoformat()
        }
        
        result = self._create_record("documents", doc_id, doc_data)
        
        if result.get("success"):
            return {
                "document_id": doc_id,
                "status": "uploaded",
                "document": result["record"]
            }
        
        return result
    
    def list_documents(
        self,
        document_type: Optional[str] = None,
        year: Optional[int] = None,
        tag: Optional[str] = None
    ) -> dict:
        """
        List business documents.
        
        Args:
            document_type: Filter by type
            year: Filter by year
            tag: Filter by tag
        
        Returns:
            List of documents
        """
        def filter_func(doc: dict) -> bool:
            if document_type and doc.get("type") != document_type:
                return False
            if year and doc.get("year") != year:
                return False
            if tag and tag not in doc.get("tags", []):
                return False
            return True
        
        result = self._list_records("documents", filter_func, sort_key="upload_date", reverse=True)
        
        if result.get("success"):
            documents = result["records"]
            
            summary = {
                "total": len(documents),
                "by_type": {},
                "by_year": {}
            }
            
            for doc in documents:
                doc_type = doc.get("type", "unknown")
                summary["by_type"][doc_type] = summary["by_type"].get(doc_type, 0) + 1
                
                doc_year = doc.get("year")
                if doc_year:
                    summary["by_year"][doc_year] = summary["by_year"].get(doc_year, 0) + 1
            
            return {
                "documents": documents,
                "summary": summary
            }
        
        return result
    
    def get_tax_summary(self, year: Optional[int] = None) -> dict:
        """
        Get comprehensive tax summary for a year.
        
        Args:
            year: Tax year
        
        Returns:
            Tax summary with deadlines and estimates
        """
        if year is None:
            year = Config.TAX_YEAR
        
        # Get deadlines
        deadlines_result = self.get_tax_deadlines(year=year, upcoming_only=False)
        
        # Get entity info
        entity = self._data.get("entity_info", {})
        
        # Calculate annual estimates for each quarter
        quarterly_estimates = []
        for q in range(1, 5):
            estimate = self.calculate_quarterly_estimate(quarter=q, year=year)
            quarterly_estimates.append(estimate)
        
        return {
            "year": year,
            "entity": entity,
            "deadlines": deadlines_result.get("deadlines", []),
            "quarterly_estimates": quarterly_estimates,
            "notes": [
                "Review with tax professional",
                "Keep all receipts and documentation",
                "Track mileage for vehicle deductions",
                "Consider home office deduction if applicable"
            ]
        }


# Standalone functions for MCP tool interface
_server_instance = None

def _get_server() -> LLCOpsServer:
    """Get or create server instance."""
    global _server_instance
    if _server_instance is None:
        _server_instance = LLCOpsServer()
    return _server_instance


def get_entity_info() -> dict:
    """Get LLC entity info."""
    return _get_server().get_entity_info()


def update_entity_info(**updates) -> dict:
    """Update LLC entity info."""
    return _get_server().update_entity_info(**updates)


def get_tax_deadlines(**kwargs) -> dict:
    """Get tax deadlines."""
    return _get_server().get_tax_deadlines(**kwargs)


def calculate_quarterly_estimate(**kwargs) -> dict:
    """Calculate quarterly tax estimate."""
    return _get_server().calculate_quarterly_estimate(**kwargs)


def add_compliance_item(**kwargs) -> dict:
    """Add compliance item."""
    return _get_server().add_compliance_item(**kwargs)


def get_compliance_checklist(**kwargs) -> dict:
    """Get compliance checklist."""
    return _get_server().get_compliance_checklist(**kwargs)


def complete_compliance_item(**kwargs) -> dict:
    """Complete compliance item."""
    return _get_server().complete_compliance_item(**kwargs)


def upload_document(**kwargs) -> dict:
    """Upload/register a document."""
    return _get_server().upload_document(**kwargs)


def list_documents(**kwargs) -> dict:
    """List documents."""
    return _get_server().list_documents(**kwargs)


def get_tax_summary(**kwargs) -> dict:
    """Get tax summary."""
    return _get_server().get_tax_summary(**kwargs)


def get_server_info() -> dict:
    """Get server info."""
    return _get_server().get_info()


if __name__ == "__main__":
    server = LLCOpsServer()
    print("LLC Ops Server - Business Operations & Compliance MCP Server")
    print(f"Data file: {server.data_path}")
    info = server.get_info()
    print(f"Available tools: {', '.join(info['tools'])}")
