# AndisMCP - Playwright Test Generator

Ein MCP (Model Context Protocol) Server zur automatischen Generierung von Playwright TypeScript-Tests mit KI-Unterstützung.

## 📋 Übersicht

AndisMCP ist ein intelligenter Server, der Websites crawlt, Page Object Models erstellt und automatisch Playwright-Tests generiert. Das Tool nutzt LangGraph und OpenAI, um qualitativ hochwertige, wartbare Test-Suites zu erstellen.

## ✨ Features

- 🔍 **Website Crawling**: Automatisches Entdecken und Analysieren von Webseiten
- 🎯 **UI-Modell Extraktion**: Erkennung von Buttons, Forms, Links und anderen UI-Elementen
- 📝 **Page Object Model Generation**: Automatische Erstellung von POMs
- 🧪 **Test-Generierung**: Intelligente Erstellung von Playwright TypeScript-Tests
- 🔧 **Syntax Repair**: Automatische Korrektur von Syntax-Fehlern
- ✅ **Validierung**: Überprüfung von generierten POMs

## 📦 Voraussetzungen

- **Python**: >= 3.10
- **Node.js**: >= 18.x (für Playwright)
- **OpenAI API Key**: Für die KI-gestützte Generierung

## 🚀 Installation

### 1. Repository klonen

```bash
git clone https://github.com/Andrejtr4/AndisMCP.git
cd DerBesteMCP
```

### 2. Python Dependencies installieren

```bash
# Virtuelle Umgebung erstellen (empfohlen)
python3 -m venv venv
source venv/bin/activate  # Auf macOS/Linux

# Dependencies installieren
pip install -r requirements.txt
```

### 3. Playwright installieren

```bash
# Playwright Browser installieren
playwright install chromium
```

### 4. Node.js Dependencies installieren (für Tests)

```bash
npm install
```

### 5. Umgebungsvariablen konfigurieren

Erstelle eine `.env`-Datei im Projektverzeichnis:

```bash
# .env
OPENAI_API_KEY=dein-openai-api-key
```

## 🎮 Verwendung

### Als MCP Server starten

Der Server kann als MCP-Server gestartet werden und bietet folgende Tools:

```bash
python src/mcp_server.py
```

### Verfügbare Tools

#### 1. **generate_tests_full** - Komplette Pipeline
Crawlt eine Website und generiert vollständige Test-Suites.

```python
{
  "url": "https://example.com",
  "max_pages": 10,
  "stories": "Optional: User Stories zur Testgenerierung"
}
```

#### 2. **crawl_links** - Links crawlen
Entdeckt alle Links auf einer Website.

```python
{
  "base_url": "https://example.com"
}
```

#### 3. **scan_site** - Website scannen
Analysiert die Struktur einer URL.

```python
{
  "url": "https://example.com/page"
}
```

#### 4. **extract_model** - UI-Modell extrahieren
Extrahiert UI-Elemente (Buttons, Forms, etc.).

```python
{
  "url": "https://example.com/page",
  "name": "LoginPage"
}
```

#### 5. **generate_pom** - Page Object Model generieren
Erstellt ein POM aus einem UI-Modell.

```python
{
  "name": "LoginPage",
  "model": { /* UI-Modell */ }
}
```

#### 6. **verify_pom** - POM validieren
Überprüft eine POM-Datei.

```python
{
  "pom_path": "tests/pages/LoginPage.ts"
}
```

#### 7. **repair_file** - Syntax reparieren
Korrigiert Syntax-Fehler in generierten Dateien.

```python
{
  "file_path": "tests/pages/LoginPage.ts",
  "error_message": "Optional: Fehlermeldung"
}
```

#### 8. **quick_start** - Schnell-Demo
Generiert Tests für `the-internet.herokuapp.com` (2 Seiten).

```python
{}
```

## 📝 Playwright Tests ausführen

Nach der Test-Generierung können die Tests ausgeführt werden:

```bash
# Alle Tests ausführen
npm test

# Tests mit UI
npm run test:ui

# Tests im Browser (headed mode)
npm run test:headed

# Tests debuggen
npm run test:debug
```

## 🏗️ Projektstruktur

```
DerBesteMCP/
├── src/
│   ├── mcp_server.py          # Haupt-MCP-Server
│   ├── core/                  # Kernfunktionalität
│   │   ├── pipeline.py        # Hauptpipeline
│   │   ├── config.py          # Konfiguration
│   │   ├── schemas.py         # Datenstrukturen
│   │   └── prompts.py         # LLM-Prompts
│   └── tools/                 # MCP Tools
│       ├── crawl_links.py
│       ├── scan_site.py
│       ├── extract_model.py
│       ├── generate_pom.py
│       ├── generate_tests_ts.py
│       ├── verify_pom.py
│       └── repair.py
├── tests/                     # Generierte Tests
├── playwright.config.ts       # Playwright-Konfiguration
├── package.json               # Node.js Dependencies
├── requirements.txt           # Python Dependencies
└── pyproject.toml            # Python Projekt-Konfiguration
```

## 🔧 Konfiguration

### Playwright-Konfiguration

Die Playwright-Konfiguration befindet sich in `playwright.config.ts`. Hier können Browser, Timeouts und weitere Einstellungen angepasst werden.

### Pipeline-Konfiguration

Die Pipeline-Einstellungen können in `src/core/config.py` angepasst werden:
- LLM-Modell (Standard: gpt-4)
- Output-Verzeichnisse
- Timeout-Einstellungen

## 🤝 Integration mit Claude Desktop / VS Code

Um AndisMCP mit Claude Desktop oder VS Code zu verwenden, füge den Server zur MCP-Konfiguration hinzu:

```json
{
  "mcpServers": {
    "andismcp": {
      "command": "python",
      "args": ["/pfad/zu/DerBesteMCP/src/mcp_server.py"],
      "env": {
        "OPENAI_API_KEY": "dein-api-key"
      }
    }
  }
}
```

## 📄 Lizenz

ISC

## 👤 Autor

Andreas

## 🐛 Fehlersuche

### "Playwright not found"
```bash
playwright install chromium
```

### "OpenAI API Error"
Überprüfe, ob dein API-Key in der `.env`-Datei korrekt gesetzt ist.

### "Module not found"
```bash
pip install -r requirements.txt
```

## 📚 Weitere Ressourcen

- [Playwright Dokumentation](https://playwright.dev)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [LangGraph Dokumentation](https://langchain-ai.github.io/langgraph/)

---

**Happy Testing! 🎭**
