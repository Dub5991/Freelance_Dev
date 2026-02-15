"""
Base MCP Server Class

Provides shared functionality for all MCP servers including:
- JSON-based data persistence
- Logging configuration
- Error handling
- Common utilities
"""

import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Union

from ..config import Config
from ..utils import load_json, save_json, setup_logging


class BaseMCPServer(ABC):
    """Base class for all MCP servers with shared functionality."""
    
    def __init__(self, server_name: str, data_file: Optional[str] = None):
        """
        Initialize the base server.
        
        Args:
            server_name: Name of the server (e.g., 'work', 'client', 'billing')
            data_file: Custom data file name (defaults to {server_name}_data.json)
        """
        self.server_name = server_name
        self.data_file = data_file or f"{server_name}_data.json"
        self.data_path = Config.DATA_DIR / self.data_file
        
        # Set up logging
        self.logger = setup_logging(
            f"mcp.{server_name}",
            Config.LOG_FILE,
            Config.LOG_LEVEL
        )
        
        # Ensure data directory exists
        Config.ensure_directories()
        
        # Initialize data storage
        self._data: dict[str, Any] = {}
        self._load_data()
        
        self.logger.info(f"{server_name} server initialized")
    
    def _load_data(self) -> None:
        """Load data from JSON file."""
        try:
            self._data = load_json(self.data_path, default={})
            self.logger.debug(f"Loaded data from {self.data_path}")
        except Exception as e:
            self.logger.error(f"Failed to load data: {e}")
            self._data = {}
    
    def _save_data(self) -> bool:
        """
        Save data to JSON file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            success = save_json(self.data_path, self._data)
            if success:
                self.logger.debug(f"Saved data to {self.data_path}")
            return success
        except Exception as e:
            self.logger.error(f"Failed to save data: {e}")
            return False
    
    def _get_collection(self, collection_name: str) -> dict:
        """
        Get a collection from data store.
        
        Args:
            collection_name: Name of the collection
        
        Returns:
            Collection dictionary
        """
        if collection_name not in self._data:
            self._data[collection_name] = {}
        return self._data[collection_name]
    
    def _set_collection(self, collection_name: str, data: dict) -> None:
        """
        Set a collection in data store.
        
        Args:
            collection_name: Name of the collection
            data: Collection data
        """
        self._data[collection_name] = data
    
    def _create_record(
        self,
        collection_name: str,
        record_id: str,
        data: dict,
        validate: bool = True
    ) -> dict:
        """
        Create a new record in a collection.
        
        Args:
            collection_name: Collection to add record to
            record_id: Unique record identifier
            data: Record data
            validate: Whether to validate before saving
        
        Returns:
            Response dictionary with status and data
        """
        collection = self._get_collection(collection_name)
        
        if record_id in collection:
            return {
                "error": f"Record '{record_id}' already exists in {collection_name}"
            }
        
        # Add metadata
        record = {
            **data,
            "id": record_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        collection[record_id] = record
        self._set_collection(collection_name, collection)
        
        if self._save_data():
            self.logger.info(f"Created {collection_name} record: {record_id}")
            return {
                "success": True,
                "id": record_id,
                "record": record
            }
        else:
            return {
                "error": f"Failed to save {collection_name} record"
            }
    
    def _read_record(self, collection_name: str, record_id: str) -> dict:
        """
        Read a record from a collection.
        
        Args:
            collection_name: Collection to read from
            record_id: Record identifier
        
        Returns:
            Record data or error
        """
        collection = self._get_collection(collection_name)
        
        if record_id not in collection:
            return {
                "error": f"Record '{record_id}' not found in {collection_name}"
            }
        
        return {
            "success": True,
            "record": collection[record_id]
        }
    
    def _update_record(
        self,
        collection_name: str,
        record_id: str,
        updates: dict
    ) -> dict:
        """
        Update a record in a collection.
        
        Args:
            collection_name: Collection containing the record
            record_id: Record identifier
            updates: Fields to update
        
        Returns:
            Response with updated record
        """
        collection = self._get_collection(collection_name)
        
        if record_id not in collection:
            return {
                "error": f"Record '{record_id}' not found in {collection_name}"
            }
        
        record = collection[record_id]
        record.update(updates)
        record["updated_at"] = datetime.now().isoformat()
        
        collection[record_id] = record
        self._set_collection(collection_name, collection)
        
        if self._save_data():
            self.logger.info(f"Updated {collection_name} record: {record_id}")
            return {
                "success": True,
                "record": record
            }
        else:
            return {
                "error": f"Failed to save {collection_name} record"
            }
    
    def _delete_record(self, collection_name: str, record_id: str) -> dict:
        """
        Delete a record from a collection.
        
        Args:
            collection_name: Collection containing the record
            record_id: Record identifier
        
        Returns:
            Response indicating success or failure
        """
        collection = self._get_collection(collection_name)
        
        if record_id not in collection:
            return {
                "error": f"Record '{record_id}' not found in {collection_name}"
            }
        
        deleted_record = collection.pop(record_id)
        self._set_collection(collection_name, collection)
        
        if self._save_data():
            self.logger.info(f"Deleted {collection_name} record: {record_id}")
            return {
                "success": True,
                "deleted": deleted_record
            }
        else:
            return {
                "error": f"Failed to save after deleting {collection_name} record"
            }
    
    def _list_records(
        self,
        collection_name: str,
        filter_func: Optional[callable] = None,
        sort_key: Optional[str] = None,
        reverse: bool = False
    ) -> dict:
        """
        List records in a collection with optional filtering and sorting.
        
        Args:
            collection_name: Collection to list
            filter_func: Optional function to filter records
            sort_key: Optional key to sort by
            reverse: Reverse sort order
        
        Returns:
            List of records
        """
        collection = self._get_collection(collection_name)
        records = list(collection.values())
        
        # Apply filter
        if filter_func:
            records = [r for r in records if filter_func(r)]
        
        # Apply sort
        if sort_key:
            try:
                records.sort(key=lambda r: r.get(sort_key, ""), reverse=reverse)
            except Exception as e:
                self.logger.warning(f"Failed to sort by {sort_key}: {e}")
        
        return {
            "success": True,
            "records": records,
            "count": len(records)
        }
    
    def _search_records(
        self,
        collection_name: str,
        search_fields: list[str],
        query: str
    ) -> dict:
        """
        Search records in a collection.
        
        Args:
            collection_name: Collection to search
            search_fields: Fields to search in
            query: Search query
        
        Returns:
            Matching records
        """
        collection = self._get_collection(collection_name)
        query_lower = query.lower()
        
        matches = []
        for record in collection.values():
            for field in search_fields:
                field_value = str(record.get(field, "")).lower()
                if query_lower in field_value:
                    matches.append(record)
                    break
        
        return {
            "success": True,
            "records": matches,
            "count": len(matches),
            "query": query
        }
    
    def get_stats(self) -> dict:
        """
        Get statistics about the data store.
        
        Returns:
            Statistics dictionary
        """
        stats = {
            "server": self.server_name,
            "data_file": str(self.data_path),
            "collections": {}
        }
        
        for collection_name, collection in self._data.items():
            if isinstance(collection, dict):
                stats["collections"][collection_name] = len(collection)
        
        return stats
    
    @abstractmethod
    def get_info(self) -> dict:
        """
        Get server information and available tools.
        Must be implemented by each server.
        
        Returns:
            Server metadata
        """
        pass
    
    def health_check(self) -> dict:
        """
        Check server health.
        
        Returns:
            Health status
        """
        try:
            # Test data persistence
            test_write = self._save_data()
            
            return {
                "healthy": test_write,
                "server": self.server_name,
                "data_file": str(self.data_path),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "healthy": False,
                "server": self.server_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
