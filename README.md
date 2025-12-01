# 🎭 Playwright Test Generator MCP# 🎭 Playwright Test Generator MCP



AI-powered TypeScript Playwright Test Generator als MCP Server für VS Code, Claude & Cursor.Automatische Generierung von **TypeScript Playwright Tests** mit KI - als MCP Server für VS Code, Claude & Cursor.



## Was macht das?> � **[Dependencies & Setup](REQUIREMENTS.md)** | 📂 **[Projekt-Struktur](STRUCTURE.md)** | 🔄 **[Workflow-Guide](WORKFLOW.md)** | ✨ **[Features](IMPROVEMENTS.md)**



1. **Crawlt** eine Website und findet alle Links## 📋 Was macht das?

2. **Scannt** jede Seite und extrahiert das DOM

3. **Analysiert** mit GPT-4 alle interaktiven ElementeDieser MCP Server:

4. **Generiert** Python POMs (intern)1. **Crawlt** eine Website und findet alle Links

5. **Erstellt** TypeScript Playwright Tests2. **Scannt** jede Seite und extrahiert das DOM

6. **Öffnet** automatisch Playwright UI 🎭3. **Analysiert** mit GPT-4 alle interaktiven Elemente

4. **Generiert** Page Object Models (POMs) in **Python**

---5. **Erstellt** automatisch **TypeScript Playwright Tests** basierend auf den Python POMs

6. **Öffnet** automatisch die Playwright UI nach erfolgreicher Test-Generierung 🎭

## 🚀 Quick Start

**Ergebnis:** Komplette Test-Suite in Sekunden statt Stunden!

### Installation

```bash## 🎯 Quick Start

# All-in-One Setup

./scripts/setup_all.sh> 📦 **[Alle Dependencies & Requirements](REQUIREMENTS.md)**



# Oder manuell:### 1. One-Command Installation ⚡

python -m venv venv

source venv/bin/activate```bash

pip install -e .# Installiert alles automatisch (Python + TypeScript + Playwright)

cd out && npm install && npx playwright install./scripts/setup_all.sh

``````



### API Key**Oder manuell:**

```bash

echo "OPENAI_API_KEY=sk-your-key-here" > .env```bash

```# Python Setup

python -m venv venv

### MCP Server startensource venv/bin/activate

```bashpip install -e .

./scripts/start_mcp.shplaywright install chromium

```

# TypeScript Setup

### In Claude/VS Code einbindencd out

npm install

**VS Code** (`.vscode/mcp.json`):npx playwright install

```json```

{

  "mcpServers": {### 2. API Key konfigurieren

    "playwright-test-gen": {

      "command": "/Users/your-path/DerBesteMCP/venv/bin/python",```bash

      "args": ["/Users/your-path/DerBesteMCP/src/mcp_server.py"]# .env Datei wird automatisch erstellt, nur noch API Key eintragen:

    }echo "OPENAI_API_KEY=sk-your-api-key-here" > .env

  }```

}

```### 3. MCP Server starten



**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):```bash

```json./scripts/start_mcp.sh

{# oder direkt: python src/mcp_server.py

  "mcpServers": {```

    "playwright-test-gen": {

      "command": "/Users/your-path/DerBesteMCP/venv/bin/python",### 4. In VS Code / Claude / Cursor einbinden

      "args": ["/Users/your-path/DerBesteMCP/src/mcp_server.py"]

    }Füge in deine MCP-Konfiguration ein:

  }

}**VS Code** (`.vscode/mcp.json`):

``````json

{

---  "mcpServers": {

    "playwright-test-gen": {

## 🎯 Verfügbare Tools      "command": "/Users/dein-pfad/DerBesteMCP/venv/bin/python",

      "args": ["/Users/dein-pfad/DerBesteMCP/src/mcp_server.py"]

### `generate_tests_full` - Komplette Pipeline    }

```  }

generate_tests_full(}

  url="https://example.com",```

  max_pages=10,

  stories="Optional: User stories for guidance"**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):

)```json

```{

  "mcpServers": {

**Workflow:**    "playwright-test-gen": {

1. Crawlt Website      "command": "/Users/dein-pfad/DerBesteMCP/venv/bin/python",

2. Erstellt Python POMs (intern)      "args": ["/Users/dein-pfad/DerBesteMCP/src/mcp_server.py"]

3. Generiert TypeScript Tests:    }

   - ✅ Happy Path Tests  }

   - ❌ Validation Error Tests}

   - 🔄 Edge Case Tests```

   - 🎹 Keyboard Navigation Tests

   - ♿ Accessibility Tests## 🛠️ Verfügbare Tools

4. Öffnet automatisch Playwright UI

### `generate_tests_full` 🎯

### `quick_start` - DemoKomplette Pipeline: Crawlt Website, generiert POMs & Tests mit AI-Enhanced Quality

```

quick_start()```

```generate_tests_full(

Generiert Tests für `the-internet.herokuapp.com` (5 Seiten)  url="https://example.com",

  max_pages=10,

### Einzelne Tools  stories="Optional: User stories for test guidance"

- `crawl_links(base_url)` - Links finden)

- `scan_site(url)` - DOM scannen```

- `extract_model(url, name)` - UI-Elemente extrahieren

- `generate_pom(name, model)` - Python POM erstellen**Workflow:**

- `verify_pom(pom_path)` - POM validieren1. POMs werden in **Python** erstellt (mit AI-Enhancement)

- `repair_file(file_path, error_message)` - Code reparieren2. Basierend auf den Python-POMs werden **TypeScript Playwright Tests** generiert

3. Tests werden intelligent mit GPT-4 erstellt:

---   - ✅ Happy Path Tests

   - ❌ Error Case Tests  

## 📁 Projekt-Struktur   - 🔄 Edge Case Tests

   - 🎹 Keyboard Navigation Tests

```   - ♿ Accessibility Tests

DerBesteMCP/   - Automatische Test-Szenario-Erkennung basierend auf Page-Type

├── README.md              # Diese Datei4. Nach erfolgreicher Generierung öffnet sich automatisch die **Playwright UI** 🎭

├── REQUIREMENTS.md        # Detaillierte Dependencies

├── .env                   # API Keys### `quick_start` 🚀

├── pyproject.toml         # Python DependenciesDemo mit the-internet.herokuapp.com (5 Seiten)

│

├── scripts/```

│   ├── setup_all.sh       # Komplettes Setupquick_start()

│   └── start_mcp.sh       # MCP Server starten```

│

├── src/### Einzelne Tools (für manuelle Kontrolle):

│   ├── mcp_server.py      # MCP Server (Einstiegspunkt)- `crawl_links(base_url)` - Links finden

│   ├── core/- `scan_site(url)` - DOM scannen

│   │   ├── pipeline.py    # LangGraph Workflow- `extract_model(url, name)` - UI-Elemente extrahieren

│   │   ├── schemas.py     # Data Models- `generate_pom(name, model)` - **Python POM** erstellen (mit AI-Enhancement)

│   │   ├── prompts.py     # LLM Prompts- `verify_pom(pom_path)` - POM validieren

│   │   ├── test_prompts_ts.py # TypeScript Test Prompts- `repair_file(file_path, error_message)` - Code reparieren

│   │   ├── config.py      # Konfiguration

│   │   └── colors.py      # Terminal Output**Hinweis:** TypeScript Tests werden automatisch in der Pipeline generiert!

│   └── tools/

│       ├── crawl_links.py## 📁 Struktur

│       ├── scan_site.py

│       ├── extract_model.pySiehe **[STRUCTURE.md](STRUCTURE.md)** für die komplette Projekt-Struktur.

│       ├── generate_pom.py

│       ├── generate_tests_ts.py**Wichtigste Verzeichnisse:**

│       ├── verify_pom.py- `src/` - Python Code (MCP Server, Pipeline, Tools)

│       └── repair.py- `out/` - Generierte Tests (Python POMs + TypeScript Tests)

│- `scripts/` - Setup & Start Scripts

└── out/                   # Generierte Dateien

    ├── poms/              # Python POMs (intern)## 🎨 Beispiel-Usage

    ├── tests/             # TypeScript Tests ✅

    ├── playwright.config.ts**In VS Code Chat / Claude:**

    ├── package.json

    └── tsconfig.json```

```Generiere Tests für https://example.com mit maximal 5 Seiten

```

---

Der Server wird:

## 🎬 Beispiel1. ✅ 5 Links crawlen

2. ✅ Jede Seite scannen

**In Claude/VS Code:**3. ✅ UI-Elemente mit GPT-4 extrahieren

```4. ✅ POMs generieren (`out/poms/`)

Generiere Tests für https://example.com mit maximal 5 Seiten5. ✅ Tests generieren (`out/tests/`)

```

**Ergebnis:**

**Output:**```python

```# out/poms/HomePage.py

out/class HomePage:

├── poms/    def __init__(self, page: Page):

│   ├── HomePage.py        self.page = page

│   ├── LoginPage.py        self.loginButton = self.page.get_by_role("button", name="Login")

│   └── CheckoutPage.py        self.searchInput = self.page.get_by_placeholder("Search...")

└── tests/    

    ├── homepage.spec.ts     ✅    def goto(self):

    ├── loginpage.spec.ts    ✅        self.page.goto("https://example.com")

    └── checkoutpage.spec.ts ✅

```# out/tests/test_homepage.py

def test_homepage_basic(page: Page):

**Playwright UI öffnet sich automatisch** 🎭    from out.poms.HomePage import HomePage

    pom = HomePage(page)

---    pom.goto()

    assert pom.page is not None

## 📦 Dependencies```



### Python (pyproject.toml)## 🔧 Technologie-Stack

- `langgraph` - Workflow orchestration

- `langchain-openai` - GPT-4 integration- **MCP SDK** - Model Context Protocol für Tool-Integration

- `playwright` - Browser automation- **LangGraph** - Workflow-Orchestrierung (Crawl → Scan → Extract → Generate)

- `modelcontextprotocol` - MCP Server- **LangChain** - LLM-Integration

- `pydantic` - Data validation- **OpenAI GPT-4** - UI-Element-Extraktion & Code-Repair

- `beautifulsoup4` - HTML parsing- **Playwright** - Browser-Automatisierung & DOM-Scanning

- `python-dotenv` - Environment variables- **BeautifulSoup** - HTML-Parsing

- **Pydantic** - Datenvalidierung

### TypeScript (out/package.json)

- `@playwright/test` - Playwright Test framework## 📝 Dependencies

- `typescript` - TypeScript compiler

- `@types/node` - Node.js types```toml

mcp >= 0.1.0

### Environment Variableslanggraph >= 0.0.28

- `OPENAI_API_KEY` - Required für AI-Generierunglangchain-openai >= 0.1.0

playwright >= 1.40.0

---beautifulsoup4 >= 4.12.0

python-dotenv >= 1.0.0

## 🔧 Manuelle Test-Ausführungpydantic >= 2.0.0

```

```bash

cd out## 🐛 Troubleshooting



# Playwright UI (empfohlen)### Server startet nicht

npx playwright test --ui```bash

# Prüfe Dependencies

# Headlesspip list | grep -E "mcp|langgraph|playwright"

npx playwright test

# Neu installieren

# Mit Browserpip install -e . --force-reinstall

npx playwright test --headed```



# Debug Mode### API Key Fehler

npx playwright test --debug```bash

```# Prüfe .env Datei

cat .env

---# OPENAI_API_KEY muss gesetzt sein

```

## 🎯 Workflow

### Playwright Browser fehlt

``````bash

URL eingebenplaywright install chromium

    ↓```

Crawl Website

    ↓### Import Errors

Scan Pages (DOM)```bash

    ↓# Stelle sicher dass venv aktiviert ist

Extract Elements (GPT-4)source venv/bin/activate

    ↓

Generate Python POMs# Prüfe Python-Pfad

    ↓which python

Generate TypeScript Tests (GPT-4)# Sollte: /Users/.../DerBesteMCP/venv/bin/python

    ↓```

Open Playwright UI

    ↓## 🚀 Development

Ready to Test! 🎉

``````bash

# Tests durchführen (optional)

---python scripts/test_mcp.py



## 🐛 Troubleshooting# Setup verifizieren (optional)

./scripts/verify_setup.sh

### "OPENAI_API_KEY not set"

```bash# Code formatieren

echo "OPENAI_API_KEY=sk-your-key" > .envblack src/

```ruff check src/



### "playwright not found"# Logs anschauen

```bash# MCP Server loggt nach stderr - in VS Code/Claude sichtbar

pip install playwright```

playwright install chromium

```## ✨ Neue Features (v2.0)



### "npx: command not found"### 🎯 AI-Enhanced Test Generation

Installiere Node.js: https://nodejs.org/Tests werden nicht mehr aus Templates generiert, sondern intelligent mit GPT-4:

- **Page-Type Detection**: Erkennt Login, Checkout, Search, Form Pages

### Python Import Errors- **Scenario Extraction**: Findet automatisch relevante Test-Szenarien

```bash- **Comprehensive Tests**: Happy Path + Error Cases + Edge Cases

source venv/bin/activate- **Best Practices**: Playwright `expect()`, descriptive names, proper waits

pip install -e .

```### 🎨 POM Improvement Tool

Neues `improve_pom` Tool verbessert existierende POMs:

---- Bessere Locator-Strategien

- Helper-Methoden für häufige Aktionen

## 📚 Weitere Dokumentation- Explicit Waits und Validation-Helpers

- Vollständige Dokumentation

Siehe **[REQUIREMENTS.md](REQUIREMENTS.md)** für:

- Detaillierte Installation### ⚙️ Konfigurierbare Test-Qualität

- Alle Dependencies```python

- System Requirementsfrom src.core.config import TestGenerationConfig

- Common Issues & Solutions

# Basic: Nur Happy Path

---config = TestGenerationConfig.basic()



## ✨ Features# Comprehensive: Alles inkl. Accessibility

config = TestGenerationConfig.comprehensive()

- ✅ **AI-Powered**: GPT-4 generiert intelligente Tests```

- 🎭 **TypeScript**: Professional Playwright Tests

- 🚀 **Automatisch**: Von URL zu Tests in Minuten📖 **Mehr Details**: Siehe [IMPROVEMENTS.md](IMPROVEMENTS.md)

- 🎨 **UI Integration**: Playwright UI öffnet automatisch

- 🔄 **Best Practices**: 5 Test-Cases pro Page## 📄 Lizenz

- 📦 **MCP Server**: Integration in Claude & VS Code

MIT

---

## 🤝 Contributing

**Version:** 1.0.0 | **License:** MIT

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
