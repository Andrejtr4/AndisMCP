import sys
from pathlib import Path
from typing import Any

# Projekt zum Python-Pfad hinzufügen, damit Importe funktionieren
sys.path.insert(0, str(Path(__file__).parent.parent))

import anyio
import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server

# Importiere die Hauptpipeline und Hilfsfunktionen
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
    """Haupteinstiegspunkt des MCP-Servers."""
    # Verbindet die Pipeline
    pipeline = PlaywrightPipeline()
    
    # Erstellt den MCP-Server (AndisMCP)
    app = Server("AndisMCP")

    # Regestriert die Tools für den MCP Server
    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        """Gibt die Liste aller verfügbaren Tools zurück."""
        return [
            # Tool 1: Vollständige Test-Generierung
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
            # Tool 2: Links auf einer Website crawlen
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
            # Tool 3: Website scannen und analysieren
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
            # Tool 4: UI-Modell aus Webseite extrahieren
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
            # Tool 5: Page Object Model generieren
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
            # Tool 6: Page Object Model validieren
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
            # Tool 7: Syntax-Fehler in generierten Dateien reparieren
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
            # Tool 8: Schnell-Demo mit vordefinierten Einstellungen
            types.Tool(
                name="quick_start",
                description="Quick demo: Generate tests for the-internet.herokuapp.com (2 pages)",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
        ]

    # Führt die Logik der Tools aus 
    @app.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.ContentBlock]:
        """Behandelt alle Tool-Aufrufe und führt die entsprechende Logik aus."""
        
        # 1: Vollständige Test-Generierung
        if name == "generate_tests_full":
            # Hole die URL aus den Argumenten
            url = arguments.get("url")
            if not url:
                raise ValueError("URL is required")
            
            # Hole optionale Parameter mit Standardwerten
            max_pages = arguments.get("max_pages", 10)
            stories = arguments.get("stories", "")

            # Führe die komplette Pipeline aus
            result = await pipeline.execute(url, max_pages, stories)
            
            response_text = f"""Test Generation Complete ✅

Summary:
- Total pages processed: {result.total_processed}
- Errors encountered: {result.total_errors}
- Output directory: out/ """

            return [types.TextContent(type="text", text=response_text)]

        #2: Links crawlen 
        elif name == "crawl_links":
            base_url = arguments.get("base_url")
            if not base_url:
                raise ValueError("base_url is required")
            
            # Crawle alle Links auf der Website
            result = await crawl_links(base_url)
            links = result.get('links', [])
            
            # Erstelle eine übersichtliche Antwort (max. 15 Links anzeigen)
            response_text = f"Found {len(links)} links\n" + "\n".join(f"• {link}" for link in links[:15])
            if len(links) > 15:
                response_text += f"\n... and {len(links)-15} more"
            return [types.TextContent(type="text", text=response_text)]

        #3: Website scannen
        elif name == "scan_site":
            url = arguments.get("url")
            if not url:
                raise ValueError("url is required")
            
            # Scanne die Website und extrahiere das DOM
            result = await scan_site(url)
            response_text = f"Scanned {url}\nDOM extracted: {len(result.get('dom', ''))} chars"
            return [types.TextContent(type="text", text=response_text)]

        # 4: UI-Modell extrahieren
        elif name == "extract_model":
            url = arguments.get("url")
            name_arg = arguments.get("name")
            if not url or not name_arg:
                raise ValueError("url and name are required")
            
            # Zuerst die Seite scannen, dann Modell extrahieren
            page_data = await scan_site(url)
            result = extract_model(url, page_data.get("dom", ""))
            response_text = f"Extracted model for {name_arg}\nElements: {len(result.get('elements', []))}"
            return [types.TextContent(type="text", text=response_text)]

        # 5: Page Object Model generieren 
        elif name == "generate_pom":
            name_arg = arguments.get("name")
            model = arguments.get("model")
            if not name_arg or not model:
                raise ValueError("name and model are required")
            
            # Generiere POM aus dem UI-Modell
            result = generate_pom(name_arg, model)
            response_text = f"Generated POM: {result}"
            return [types.TextContent(type="text", text=response_text)]

        # 6: POM validieren
        elif name == "verify_pom":
            pom_path = arguments.get("pom_path")
            if not pom_path:
                raise ValueError("pom_path is required")
            
            # Überprüfe ob das POM syntaktisch korrekt ist
            is_valid, message = verify_pom(pom_path)
            status = "Valid" if is_valid else "Invalid"
            response_text = f"{status}: {pom_path}\n{message}"
            return [types.TextContent(type="text", text=response_text)]

        # 7: Datei reparieren
        elif name == "repair_file":
            file_path = arguments.get("file_path")
            error_message = arguments.get("error_message", "")
            if not file_path:
                raise ValueError("file_path is required")
            
            # Versuche Syntax-Fehler in der Datei zu beheben
            result = repair_file(file_path, error_message)
            response_text = f"Repaired: {file_path}"
            return [types.TextContent(type="text", text=response_text)]

        # 8: Schnell-Demo 
        elif name == "quick_start":
            # Führe Demo mit vordefinierter URL und 2 Seiten aus
            result = await pipeline.execute("https://the-internet.herokuapp.com", 2)
            response_text = f"""Demo Complete ✅

Summary:
- Pages processed: {result.total_processed}
- Errors: {result.total_errors}
- Output: out/
"""
            return [types.TextContent(type="text", text=response_text)]

        # Unbekanntes Tool wurde aufgerufen
        raise ValueError(f"Unknown tool: {name}")

    # Asynchrone Funktion zum Starten des Servers
    async def arun():
        """Startet den MCP-Server mit stdio-Transport."""
        async with stdio_server() as streams:
            await app.run(
                streams[0],  # Input-Stream
                streams[1],  # Output-Stream
                app.create_initialization_options()
            )

    # Server-Start mit Header-Ausgabe
    print_header("PLAYWRIGHT TEST GENERATOR MCP")
    print_success("Starting...")
    
    # Führe die async-Funktion aus
    anyio.run(arun)
    return 0


if __name__ == "__main__":
    sys.exit(main())
