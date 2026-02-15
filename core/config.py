"""
Configuration Management for Freelance LLC OS

Handles environment variables, defaults, and validation for all MCP servers.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Central configuration for the Freelance LLC OS."""
    
    # Base paths
    BASE_DIR: Path = Path(__file__).parent.parent.absolute()
    DATA_DIR: Path = BASE_DIR / "data"
    VAULT_PATH: str = os.getenv("VAULT_PATH", str(BASE_DIR / "vault"))
    
    # Stripe configuration
    STRIPE_API_KEY: Optional[str] = os.getenv("STRIPE_API_KEY")
    STRIPE_WEBHOOK_SECRET: Optional[str] = os.getenv("STRIPE_WEBHOOK_SECRET")
    
    # Business information
    LLC_NAME: str = os.getenv("LLC_NAME", "Your Freelance LLC")
    LLC_EIN: Optional[str] = os.getenv("LLC_EIN")
    LLC_STATE: Optional[str] = os.getenv("LLC_STATE")
    LLC_ADDRESS: Optional[str] = os.getenv("LLC_ADDRESS")
    
    # Billing defaults
    DEFAULT_HOURLY_RATE: float = float(os.getenv("DEFAULT_HOURLY_RATE", "150.0"))
    DEFAULT_CURRENCY: str = os.getenv("DEFAULT_CURRENCY", "USD")
    PAYMENT_TERMS_DAYS: int = int(os.getenv("PAYMENT_TERMS_DAYS", "30"))
    
    # Tax configuration
    TAX_YEAR: int = int(os.getenv("TAX_YEAR", "2024"))
    QUARTERLY_TAX_RATE: float = float(os.getenv("QUARTERLY_TAX_RATE", "0.30"))
    
    # Email notifications (optional)
    SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    EMAIL_FROM: Optional[str] = os.getenv("EMAIL_FROM")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Path = DATA_DIR / "app.log"
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        Path(cls.VAULT_PATH).mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def validate(cls) -> dict[str, list[str]]:
        """
        Validate configuration and return any warnings or errors.
        
        Returns:
            dict with 'errors' and 'warnings' lists
        """
        errors = []
        warnings = []
        
        # Check critical paths
        if not cls.BASE_DIR.exists():
            errors.append(f"Base directory not found: {cls.BASE_DIR}")
        
        # Check Stripe configuration for billing server
        if not cls.STRIPE_API_KEY:
            warnings.append("STRIPE_API_KEY not set - billing features will be limited")
        
        # Check business information
        if not cls.LLC_EIN:
            warnings.append("LLC_EIN not set - needed for tax reporting")
        
        if not cls.LLC_STATE:
            warnings.append("LLC_STATE not set - needed for compliance tracking")
        
        # Check email configuration
        if cls.SMTP_HOST and not cls.SMTP_USER:
            warnings.append("SMTP_HOST set but SMTP_USER missing")
        
        return {
            "errors": errors,
            "warnings": warnings
        }
    
    @classmethod
    def get_summary(cls) -> dict:
        """Get a summary of current configuration."""
        return {
            "base_dir": str(cls.BASE_DIR),
            "data_dir": str(cls.DATA_DIR),
            "vault_path": cls.VAULT_PATH,
            "llc_name": cls.LLC_NAME,
            "default_rate": cls.DEFAULT_HOURLY_RATE,
            "currency": cls.DEFAULT_CURRENCY,
            "tax_year": cls.TAX_YEAR,
            "stripe_configured": bool(cls.STRIPE_API_KEY),
            "email_configured": bool(cls.SMTP_HOST and cls.SMTP_USER),
        }


# Initialize directories on import
Config.ensure_directories()
