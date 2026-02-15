#!/bin/bash
# Freelance Dev OS Installation Script
# This script sets up the development environment for the Freelance LLC Operating System

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_step() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════╗"
echo "║       🚀 Freelance Dev OS Installation Script        ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Python version
print_step "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]; }; then
    print_error "Python 3.9+ is required. Current version: $PYTHON_VERSION"
    exit 1
fi

print_success "Python $PYTHON_VERSION detected"

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found. Please run this script from the project root directory."
    exit 1
fi

# Create virtual environment
print_step "Creating virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_step "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_step "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
print_success "pip upgraded"

# Install dependencies
print_step "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
print_success "Dependencies installed"

# Create necessary directories
print_step "Creating necessary directories..."

# Data directory
if [ ! -d "data" ]; then
    mkdir -p data
    print_success "Created data/ directory"
else
    print_warning "data/ directory already exists"
fi

# Ensure vault structure exists
if [ -d "vault" ]; then
    print_success "vault/ directory exists"
else
    print_warning "vault/ directory not found (should be in repo)"
fi

# Set up .env file
print_step "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success "Created .env from .env.example"
        print_warning "Please edit .env file with your actual configuration values"
    else
        print_error ".env.example not found"
        exit 1
    fi
else
    print_warning ".env file already exists. Skipping creation."
fi

# Create .gitkeep for data directory
if [ ! -f "data/.gitkeep" ]; then
    touch data/.gitkeep
    print_success "Created data/.gitkeep"
fi

# Validate installation
print_step "Validating installation..."

# Test Python imports
python3 << 'PYTHON_SCRIPT'
import sys
try:
    import dotenv
    import pydantic
    import yaml
    import pytest
    print("✓ All required Python packages imported successfully")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# Test core imports
try:
    from core.config import Config
    from core.utils import setup_logging
    print("✓ Core modules imported successfully")
except ImportError as e:
    print(f"✗ Core module import error: {e}")
    sys.exit(1)

# Test MCP server imports
try:
    from core.mcp.base_server import BaseMCPServer
    from core.mcp.work_server import get_server_info as work_info
    from core.mcp.client_server import ClientServer
    from core.mcp.billing_server import BillingServer
    print("✓ MCP servers imported successfully")
except ImportError as e:
    print(f"✗ MCP server import error: {e}")
    sys.exit(1)
PYTHON_SCRIPT

if [ $? -eq 0 ]; then
    print_success "Installation validated successfully"
else
    print_error "Installation validation failed"
    exit 1
fi

# Run a quick test
print_step "Running quick tests..."
if python3 -m pytest tests/ -q --tb=no > /dev/null 2>&1; then
    print_success "All tests passed"
else
    print_warning "Some tests failed or no tests found (this is OK if tests aren't written yet)"
fi

# Print summary
echo ""
echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════╗"
echo "║           ✓ Installation Complete!                   ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment:"
echo "     ${BLUE}source venv/bin/activate${NC}"
echo ""
echo "  2. Edit your .env file with your configuration:"
echo "     ${BLUE}nano .env${NC} or ${BLUE}vim .env${NC}"
echo ""
echo "  3. Test the installation:"
echo "     ${BLUE}python -m core.mcp.work_server${NC}"
echo ""
echo "  4. Run the test suite:"
echo "     ${BLUE}pytest tests/ -v${NC}"
echo ""
echo "  5. Read the documentation:"
echo "     ${BLUE}cat README.md${NC}"
echo "     ${BLUE}cat CLAUDE.md${NC}"
echo ""
echo "For help and documentation, see:"
echo "  - README.md (user guide)"
echo "  - CLAUDE.md (developer guide)"
echo "  - .claude/skills/ (Claude skill definitions)"
echo ""
print_success "Happy freelancing! 🚀"
