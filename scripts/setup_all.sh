#!/bin/bash

# All-in-One Setup Script für DerBesteMCP
# Installiert alle Python und TypeScript Dependencies

set -e  # Exit on error

echo "🚀 DerBesteMCP - Complete Setup"
echo "================================"
echo ""

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funktion für farbige Ausgabe
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Change to project root
cd "$(dirname "$0")/.." || exit 1
PROJECT_ROOT=$(pwd)

echo "📁 Project Root: $PROJECT_ROOT"
echo ""

# ============================================
# 1. Python Setup
# ============================================
print_status "Step 1/5: Checking Python..."

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed!"
    echo "Please install Python 3.10 or higher from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python found: $PYTHON_VERSION"

# ============================================
# 2. Virtual Environment
# ============================================
print_status "Step 2/5: Setting up Python Virtual Environment..."

if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# ============================================
# 3. Python Dependencies
# ============================================
print_status "Step 3/5: Installing Python dependencies..."

pip install --upgrade pip setuptools wheel > /dev/null 2>&1
print_success "pip updated"

print_status "Installing project dependencies (this may take a minute)..."
pip install -e . > /dev/null 2>&1
print_success "Python dependencies installed"

print_status "Installing Playwright browser..."
playwright install chromium > /dev/null 2>&1
print_success "Playwright browser installed"

# ============================================
# 4. Node.js & TypeScript Setup
# ============================================
print_status "Step 4/5: Checking Node.js..."

if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed!"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version)
print_success "Node.js found: $NODE_VERSION"

if ! command -v npm &> /dev/null; then
    print_error "npm is not installed!"
    exit 1
fi

NPM_VERSION=$(npm --version)
print_success "npm found: $NPM_VERSION"

# ============================================
# 5. TypeScript Dependencies
# ============================================
print_status "Step 5/5: Installing TypeScript dependencies..."

cd "$PROJECT_ROOT/out" || exit 1

if [ ! -f "package.json" ]; then
    print_error "package.json not found in out/ directory!"
    exit 1
fi

print_status "Installing npm packages..."
npm install > /dev/null 2>&1
print_success "TypeScript dependencies installed"

print_status "Installing Playwright browsers for TypeScript tests..."
npx playwright install > /dev/null 2>&1
print_success "Playwright browsers installed"

cd "$PROJECT_ROOT" || exit 1

# ============================================
# 6. Environment Check
# ============================================
echo ""
print_status "Checking environment configuration..."

if [ ! -f ".env" ]; then
    print_warning ".env file not found!"
    echo ""
    echo "Creating template .env file..."
    cat > .env << 'EOF'
# OpenAI API Key (Required)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional: Model configuration
# OPENAI_MODEL=gpt-4o
# OPENAI_TEMPERATURE=0.1
EOF
    print_success ".env template created"
    print_warning "Please edit .env and add your OpenAI API key!"
else
    if grep -q "sk-your-openai-api-key-here" .env; then
        print_warning ".env exists but contains placeholder API key"
        print_warning "Please edit .env and add your real OpenAI API key!"
    else
        print_success ".env file configured"
    fi
fi

# ============================================
# Summary
# ============================================
echo ""
echo "================================"
echo "🎉 Setup Complete!"
echo "================================"
echo ""
echo "📦 Installed Components:"
print_success "Python $PYTHON_VERSION + Virtual Environment"
print_success "Python packages (LangGraph, LangChain, Playwright, etc.)"
print_success "Node.js $NODE_VERSION"
print_success "TypeScript + Playwright Test Framework"
print_success "Playwright browsers (Chromium)"
echo ""

if grep -q "sk-your-openai-api-key-here" .env 2>/dev/null || [ ! -f ".env" ]; then
    echo "⚠️  Next Steps:"
    echo "   1. Edit .env file and add your OpenAI API key"
    echo "   2. Run: ./scripts/start_mcp.sh"
else
    echo "✅ Ready to use!"
    echo ""
    echo "🚀 Quick Start:"
    echo "   1. Start MCP Server: ./scripts/start_mcp.sh"
    echo "   2. Or test manually:"
    echo "      source venv/bin/activate"
    echo "      python src/mcp_server.py"
fi

echo ""
echo "📚 Documentation:"
echo "   - README.md         - Quick Start Guide"
echo "   - REQUIREMENTS.md   - All Dependencies"
echo "   - STRUCTURE.md      - Project Structure"
echo "   - WORKFLOW.md       - Detailed Workflow"
echo ""

# Return to project root
cd "$PROJECT_ROOT" || exit 1
