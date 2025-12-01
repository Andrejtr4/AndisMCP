# 🚀 Playwright Test Generator MCP

Automatische Generierung von Playwright Tests mit KI - als MCP Server für VS Code, Claude & Cursor.

## 📋 Was macht das?

Dieser MCP Server:
1. **Crawlt** eine Website und findet alle Links
2. **Scannt** jede Seite und extrahiert das DOM
3. **Analysiert** mit GPT-4 alle interaktiven Elemente
4. **Generiert** Page Object Models (POMs) in Python
5. **Erstellt** automatisch Playwright Tests

**Ergebnis:** Komplette Test-Suite in Sekunden statt Stunden!

## 🎯 Quick Start

### 1. Installation

```bash
# Repository klonen
git clone <dein-repo>
cd DerBesteMCP

# Virtual Environment erstellen
python -m venv venv
source venv/bin/activate  # macOS/Linux
# oder: venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -e .

# Playwright Browser installieren
playwright install chromium
```

### 2. API Key konfigurieren

Erstelle `.env` Datei:
```bash
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. MCP Server starten

```bash
./scripts/start_mcp.sh
# oder direkt: python src/mcp_server.py
```

### 4. In VS Code / Claude / Cursor einbinden

Füge in deine MCP-Konfiguration ein:

**VS Code** (`.vscode/mcp.json`):
```json
{
  "mcpServers": {
    "playwright-test-gen": {
      "command": "/Users/dein-pfad/DerBesteMCP/venv/bin/python",
      "args": ["/Users/dein-pfad/DerBesteMCP/src/mcp_server.py"]
    }
  }
}
```

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "playwright-test-gen": {
      "command": "/Users/dein-pfad/DerBesteMCP/venv/bin/python",
      "args": ["/Users/dein-pfad/DerBesteMCP/src/mcp_server.py"]
    }
  }
}
```

## 🛠️ Verfügbare Tools

### `generate_tests_full`
Komplette Pipeline: Crawlt Website, generiert POMs & Tests

```
generate_tests_full(
  url="https://example.com",
  max_pages=10,
  stories="Optional: User stories for test guidance"
)
```

### `quick_start`
Demo mit the-internet.herokuapp.com (5 Seiten)

```
quick_start()
```

### Einzelne Tools:
- `crawl_links(base_url)` - Links finden
- `scan_site(url)` - DOM scannen
- `extract_model(url, name)` - UI-Elemente extrahieren
- `generate_pom(name, model)` - POM erstellen
- `generate_test(pom_path, stories)` - Tests generieren
- `verify_pom(pom_path)` - POM validieren
- `repair_file(file_path, error_message)` - Code reparieren

## 📁 Struktur

```
DerBesteMCP/
├── .env                    # API Keys
├── pyproject.toml          # Dependencies
├── scripts/
│   ├── start_mcp.sh       # Server starten
│   ├── test_mcp.py        # Server testen (optional)
│   └── verify_setup.sh    # Setup prüfen (optional)
├── src/
│   ├── mcp_server.py      # MCP Server (Haupteinstieg)
│   ├── core/
│   │   ├── pipeline.py    # LangGraph Workflow
│   │   ├── schemas.py     # Datenmodelle
│   │   ├── prompts.py     # LLM Prompts
│   │   └── colors.py      # Terminal-Formatierung
│   └── tools/
│       ├── crawl_links.py    # Link-Crawler
│       ├── scan_site.py      # DOM-Scanner
│       ├── extract_model.py  # UI-Extraktion mit LLM
│       ├── generate_pom.py   # POM-Generator
│       ├── generate_tests.py # Test-Generator
│       ├── verify_pom.py     # Syntax-Checker
│       └── repair.py         # Code-Repair mit LLM
└── out/
    ├── poms/              # Generierte Page Object Models
    └── tests/             # Generierte Tests
```

## 🎨 Beispiel-Usage

**In VS Code Chat / Claude:**

```
Generiere Tests für https://example.com mit maximal 5 Seiten
```

Der Server wird:
1. ✅ 5 Links crawlen
2. ✅ Jede Seite scannen
3. ✅ UI-Elemente mit GPT-4 extrahieren
4. ✅ POMs generieren (`out/poms/`)
5. ✅ Tests generieren (`out/tests/`)

**Ergebnis:**
```python
# out/poms/HomePage.py
class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.loginButton = self.page.get_by_role("button", name="Login")
        self.searchInput = self.page.get_by_placeholder("Search...")
    
    def goto(self):
        self.page.goto("https://example.com")

# out/tests/test_homepage.py
def test_homepage_basic(page: Page):
    from out.poms.HomePage import HomePage
    pom = HomePage(page)
    pom.goto()
    assert pom.page is not None
```

## 🔧 Technologie-Stack

- **MCP SDK** - Model Context Protocol für Tool-Integration
- **LangGraph** - Workflow-Orchestrierung (Crawl → Scan → Extract → Generate)
- **LangChain** - LLM-Integration
- **OpenAI GPT-4** - UI-Element-Extraktion & Code-Repair
- **Playwright** - Browser-Automatisierung & DOM-Scanning
- **BeautifulSoup** - HTML-Parsing
- **Pydantic** - Datenvalidierung

## 📝 Dependencies

```toml
mcp >= 0.1.0
langgraph >= 0.0.28
langchain-openai >= 0.1.0
playwright >= 1.40.0
beautifulsoup4 >= 4.12.0
python-dotenv >= 1.0.0
pydantic >= 2.0.0
```

## 🐛 Troubleshooting

### Server startet nicht
```bash
# Prüfe Dependencies
pip list | grep -E "mcp|langgraph|playwright"

# Neu installieren
pip install -e . --force-reinstall
```

### API Key Fehler
```bash
# Prüfe .env Datei
cat .env
# OPENAI_API_KEY muss gesetzt sein
```

### Playwright Browser fehlt
```bash
playwright install chromium
```

### Import Errors
```bash
# Stelle sicher dass venv aktiviert ist
source venv/bin/activate

# Prüfe Python-Pfad
which python
# Sollte: /Users/.../DerBesteMCP/venv/bin/python
```

## 🚀 Development

```bash
# Tests durchführen (optional)
python scripts/test_mcp.py

# Setup verifizieren (optional)
./scripts/verify_setup.sh

# Code formatieren
black src/
ruff check src/

# Logs anschauen
# MCP Server loggt nach stderr - in VS Code/Claude sichtbar
```

## 📄 Lizenz

MIT

## 🤝 Contributing

PRs willkommen! Bitte:
1. Code so einfach wie möglich halten
2. Keine unnötigen Dependencies
3. Tests hinzufügen falls sinnvoll

## 💡 Tipps

- **Max Pages begrenzen:** Bei großen Sites `max_pages=5-10` nutzen
- **User Stories:** Bessere Tests mit `stories="Test login flow and navigation"`
- **Repair:** Bei Fehlern automatisch mit `repair_file()` fixen
- **Verify:** POMs mit `verify_pom()` vor dem Ausführen prüfen

---

**Made with ❤️ using MCP, LangGraph & GPT-4**
