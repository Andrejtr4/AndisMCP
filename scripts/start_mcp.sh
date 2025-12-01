#!/bin/bash

# 🚀 Playwright Test Generator MCP Server
# Starts the single MCP server for test generation

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT" || exit 1

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}  🚀 PLAYWRIGHT TEST GENERATOR - MCP SERVER${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check venv
if [ ! -f "venv/bin/python" ]; then
    echo -e "${YELLOW}⚠ Virtual environment not found${NC}"
    echo ""
    echo "Setup required:"
    echo "  python -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -e ."
    exit 1
fi

# Activate venv
. venv/bin/activate

echo -e "${GREEN}✓${NC} Environment ready"
echo ""
echo -e "${YELLOW}📋 Available Tools:${NC}"
echo "  • generate_tests(url, max_pages, stories)  - Generate tests for any URL"
echo "  • quick_start()                           - Demo with the-internet.herokuapp.com"
echo ""
echo -e "${YELLOW}🎯 Usage:${NC}"
echo "  1. Connect MCP server in VS Code / Claude / Cursor"
echo "  2. Use the tools above in the chat"
echo "  3. Generated files: out/poms/ and out/tests/"
echo ""
echo -e "${YELLOW}📚 Documentation:${NC}"
echo "  • Config: .vscode/mcp.json"
echo "  • Source: src/mcp_server.py"
echo "  • Docs: README.md"
echo ""
echo -e "${YELLOW}🔌 Server Status:${NC}"
echo "  Starting on stdio interface..."
echo ""

# Run the single MCP server
python src/mcp_server.py "$@"
