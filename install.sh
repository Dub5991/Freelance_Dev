#!/bin/bash

# Freelance LLC OS - Automated Installation Script
# Detects OS, installs dependencies, generates configuration

set -e  # Exit on error

echo "🚀 Freelance LLC OS - Installation"
echo "=================================="
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo "✅ Detected: Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
    echo "✅ Detected: macOS"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
    echo "✅ Detected: Windows"
else
    echo "⚠️  Unknown OS: $OSTYPE"
    echo "Proceeding with generic Linux setup..."
    OS="linux"
fi

echo ""

# Check Python
echo "📦 Checking dependencies..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python: $PYTHON_VERSION"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js not found. Some features may not work."
    echo "   Install from: https://nodejs.org/"
else
    NODE_VERSION=$(node --version)
    echo "✅ Node.js: $NODE_VERSION"
fi

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install pip3"
    exit 1
fi
echo "✅ pip3: installed"

echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt
echo "✅ Python dependencies installed"

echo ""

# Install Node dependencies (if Node is available)
if command -v npm &> /dev/null; then
    echo "📦 Installing Node.js dependencies..."
    npm install
    echo "✅ Node.js dependencies installed"
fi

echo ""

# Create .env from template if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "✅ .env file created"
    echo ""
    echo "🔴 YOUR ACTION NEEDED:"
    echo "   Edit .env file and add your information:"
    echo "   - LLC details"
    echo "   - Stripe API keys (for invoicing)"
    echo "   - Hourly rate"
    echo "   - Vault path"
    echo ""
else
    echo "✅ .env file already exists"
fi

# Create vault structure
echo "📁 Creating vault structure..."
mkdir -p vault/{00-Inbox,01-Quarter_Goals,02-Week_Priorities,03-Tasks,04-Projects}
mkdir -p vault/05-Areas/{People,Companies,Finance/{invoices,expenses,tax},Business_Dev,Career/{skills,portfolio}}
mkdir -p vault/06-Resources/{System,Templates}
mkdir -p vault/07-Archives

echo "✅ Vault structure created"
echo ""

# Generate MCP config
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VAULT_PATH="$SCRIPT_DIR/vault"

echo "🔧 Generating MCP configuration..."

# For Claude Desktop on Mac
if [ "$OS" == "mac" ]; then
    MCP_CONFIG_DIR="$HOME/Library/Application Support/Claude"
    if [ -d "$MCP_CONFIG_DIR" ]; then
        echo "Found Claude Desktop config directory"
        
        # Create config if doesn't exist
        if [ ! -f "$MCP_CONFIG_DIR/config.json" ]; then
            echo '{
  "mcpServers": {}
}' > "$MCP_CONFIG_DIR/config.json"
        fi
        
        echo "⚠️  MCP server configuration needs to be added manually to:"
        echo "   $MCP_CONFIG_DIR/config.json"
        echo ""
        echo "   See System/.mcp.json.example for template"
    fi
fi

# For Linux
if [ "$OS" == "linux" ]; then
    MCP_CONFIG_DIR="$HOME/.config/claude"
    echo "⚠️  MCP server configuration should be added to:"
    echo "   $MCP_CONFIG_DIR/config.json"
    echo ""
    echo "   See System/.mcp.json.example for template"
fi

echo ""

# Summary
echo "✅ Installation Complete!"
echo ""
echo "=========================================="
echo "NEXT STEPS:"
echo "=========================================="
echo ""
echo "1. Edit .env file with your information:"
echo "   - LLC details"
echo "   - Stripe API keys (get from dashboard.stripe.com)"
echo "   - Your hourly rate"
echo "   - Update VAULT_PATH to: $VAULT_PATH"
echo ""
echo "2. Configure MCP in your Claude client:"
echo "   - See System/.mcp.json.example"
echo "   - Replace {{VAULT_PATH}} with: $VAULT_PATH"
echo "   - Add to your MCP client config"
echo ""
echo "3. Start using the system:"
echo "   - Open Claude with MCP configured"
echo "   - Say: '/setup' to run onboarding"
echo "   - Or: 'create a task' to start tracking"
echo ""
echo "📚 Documentation:"
echo "   - System Guide: vault/06-Resources/System/System_Guide.md"
echo "   - Technical Guide: vault/06-Resources/System/Technical_Guide.md"
echo ""
echo "💡 Need help? Check the README.md or GitHub issues"
echo ""
echo "Built by devs, for devs. Let's build something great! 🚀"
