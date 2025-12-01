"""Playwright Test Generation MCP Server."""

import sys
from pathlib import Path
from typing import Any

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import anyio
import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server

from src.core.pipeline import PlaywrightPipeline
from src.core.colors import print_header, print_success, print_info
from src.tools.crawl_links import crawl_links
from src.tools.scan_site import scan_site
from src.tools.extract_model import extract_model
from src.tools.generate_pom import generate_pom
from src.tools.generate_tests_ts import generate_tests_ts
from src.tools.verify_pom import verify_pom
from src.tools.repair import repair_file


def main() -> int:
    """Main entry point."""
    # Initialize pipeline
    pipeline = PlaywrightPipeline()
    
    # Create MCP server
    app = Server("AndisMCP")

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        """Return list of available tools."""
        return [
            types.Tool(
                name="generate_tests_full",
                description="Complete pipeline: Generate Playwright tests for a website. Crawls the site, creates Page Object Models, and generates test files.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "Base URL to crawl and generate tests for",
                        },
                        "max_pages": {
                            "type": "integer",
                            "description": "Maximum number of pages to process (default: 10)",
                            "default": 10,
                        },
                        "stories": {
                            "type": "string",
                            "description": "Optional user stories to guide test generation",
                        },
                    },
                    "required": ["url"],
                },
            ),
            types.Tool(
                name="crawl_links",
                description="Crawl and discover all links on a website",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "base_url": {
                            "type": "string",
                            "description": "Base URL to start crawling from",
                        },
                    },
                    "required": ["base_url"],
                },
            ),
            types.Tool(
                name="scan_site",
                description="Scan a URL and analyze its structure",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL to scan",
                        },
                    },
                    "required": ["url"],
                },
            ),
            types.Tool(
                name="extract_model",
                description="Extract UI model from a webpage (buttons, forms, links, etc.)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL to extract model from",
                        },
                        "name": {
                            "type": "string",
                            "description": "Name for the page (e.g., 'LoginPage')",
                        },
                    },
                    "required": ["url", "name"],
                },
            ),
            types.Tool(
                name="generate_pom",
                description="Generate Page Object Model from UI model",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name for the POM (e.g., 'LoginPage')",
                        },
                        "model": {
                            "type": "object",
                            "description": "UI model extracted from page",
                        },
                    },
                    "required": ["name", "model"],
                },
            ),
            types.Tool(
                name="verify_pom",
                description="Verify and validate a Page Object Model file",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "pom_path": {
                            "type": "string",
                            "description": "Path to the POM file to verify",
                        },
                    },
                    "required": ["pom_path"],
                },
            ),
            types.Tool(
                name="repair_file",
                description="Repair syntax errors in generated files",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the file to repair",
                        },
                        "error_message": {
                            "type": "string",
                            "description": "Optional error message to help with repair",
                        },
                    },
                    "required": ["file_path"],
                },
            ),
            types.Tool(
                name="quick_start",
                description="Quick demo: Generate tests for the-internet.herokuapp.com (2 pages)",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
        ]

    @app.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.ContentBlock]:
        """Handle tool calls."""
        if name == "generate_tests_full":
            url = arguments.get("url")
            if not url:
                raise ValueError("URL is required")
            
            max_pages = arguments.get("max_pages", 10)
            stories = arguments.get("stories", "")

            result = await pipeline.execute(url, max_pages, stories)
            
            response_text = f"""Test Generation Complete ✅

Summary:
- Total pages processed: {result.total_processed}
- Errors encountered: {result.total_errors}
- Output directory: out/

Generated Files:
- Page Object Models (Python): out/poms/
- Test Files (TypeScript): out/tests/

🎭 Playwright UI is now opening automatically!

You can also run tests manually:
- npx playwright test --ui (UI mode)
- npx playwright test (headless)
- npx playwright test --headed (with browser)
"""
            return [types.TextContent(type="text", text=response_text)]

        elif name == "crawl_links":
            base_url = arguments.get("base_url")
            if not base_url:
                raise ValueError("base_url is required")
            
            result = await crawl_links(base_url)
            links = result.get('links', [])
            response_text = f"Found {len(links)} links\n" + "\n".join(f"• {link}" for link in links[:15])
            if len(links) > 15:
                response_text += f"\n... and {len(links)-15} more"
            return [types.TextContent(type="text", text=response_text)]

        elif name == "scan_site":
            url = arguments.get("url")
            if not url:
                raise ValueError("url is required")
            
            result = await scan_site(url)
            response_text = f"Scanned {url}\nDOM extracted: {len(result.get('dom', ''))} chars"
            return [types.TextContent(type="text", text=response_text)]

        elif name == "extract_model":
            url = arguments.get("url")
            name_arg = arguments.get("name")
            if not url or not name_arg:
                raise ValueError("url and name are required")
            
            # Need to scan first
            page_data = await scan_site(url)
            result = extract_model(url, page_data.get("dom", ""))
            response_text = f"Extracted model for {name_arg}\nElements: {len(result.get('elements', []))}"
            return [types.TextContent(type="text", text=response_text)]

        elif name == "generate_pom":
            name_arg = arguments.get("name")
            model = arguments.get("model")
            if not name_arg or not model:
                raise ValueError("name and model are required")
            
            result = generate_pom(name_arg, model)
            response_text = f"Generated POM: {result}"
            return [types.TextContent(type="text", text=response_text)]

        elif name == "verify_pom":
            pom_path = arguments.get("pom_path")
            if not pom_path:
                raise ValueError("pom_path is required")
            
            is_valid, message = verify_pom(pom_path)
            status = "Valid" if is_valid else "Invalid"
            response_text = f"{status}: {pom_path}\n{message}"
            return [types.TextContent(type="text", text=response_text)]

        elif name == "repair_file":
            file_path = arguments.get("file_path")
            error_message = arguments.get("error_message", "")
            if not file_path:
                raise ValueError("file_path is required")
            
            result = repair_file(file_path, error_message)
            response_text = f"Repaired: {file_path}"
            return [types.TextContent(type="text", text=response_text)]

        elif name == "quick_start":
            result = await pipeline.execute("https://the-internet.herokuapp.com", 2)
            response_text = f"""Demo Complete ✅

Summary:
- Total pages processed: {result.total_processed}
- Errors encountered: {result.total_errors}
- Output directory: out/

Generated Files:
- Page Object Models (2 POMs): out/poms/
- Test Files (2 Tests): out/tests/

🎭 Playwright UI is now opening automatically!

You can also run tests manually:
- npx playwright test --ui (UI mode)
- npx playwright test (headless)
- npx playwright test --headed (with browser)
"""
            return [types.TextContent(type="text", text=response_text)]

        raise ValueError(f"Unknown tool: {name}")

    # Run server with stdio transport
    async def arun():
        async with stdio_server() as streams:
            await app.run(
                streams[0],
                streams[1],
                app.create_initialization_options()
            )

    print_header("PLAYWRIGHT TEST GENERATOR MCP")
    print_success("Starting...")
    
    anyio.run(arun)
    return 0


if __name__ == "__main__":
    sys.exit(main())
