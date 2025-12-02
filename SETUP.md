# 🎭 AndisMCP - Automated Playwright Test Generator

AI-powered TypeScript Playwright Test Generator als MCP Server für VS Code, Claude & Cursor.

## 📋 Was macht das?

Dieser MCP Server:

1. **Crawlt** eine Website und findet alle Links
2. **Scannt** jede Seite und extrahiert das DOM
3. **Analysiert** mit GPT-4 alle interaktiven Elemente
4. **Generiert** Page Object Models (POMs) in Python
5. **Erstellt** automatisch TypeScript Playwright Tests
6. **Öffnet** automatisch die Playwright UI nach erfolgreicher Test-Generierung 🎭

**Ergebnis:** Komplette Test-Suite in Sekunden statt Stunden!

---

## 🚀 Setup auf neuem Rechner

### 1. Repository klonen

```bash
git clone https://github.com/Andrejtr4/AndisMCP.git
cd AndisMCP
```

### 2. Python Virtual Environment erstellen

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# oder
venv\Scripts\activate  # Windows
```

### 3. Python Dependencies installieren

```bash
pip install -r requirements.txt
```

### 4. Node.js Dependencies installieren

```bash
npm install
```

### 5. Playwright Browser installieren

```bash
npx playwright install
```

### 6. API Key konfigurieren

```bash
# .env Datei erstellen
echo "OPENAI_API_KEY=sk-your-api-key-here" > .env
```

### 7. VS Code MCP Extension verwenden

Die `.vscode/mcp.json` ist bereits konfiguriert und nutzt relative Pfade (`${workspaceFolder}`).
Nach dem Setup funktioniert der AndisMCP Server automatisch in VS Code!

---

## 🎯 Tests ausführen

```bash
# Alle Tests ausführen
npx playwright test

# Spezifische Test-Datei
npx playwright test tests/homepage.spec.ts

# Mit UI
npx playwright test --ui
```

## 🔧 MCP Server manuell starten (optional)

```bash
source venv/bin/activate
python src/mcp_server.py
```

---

## 📦 Verfügbare MCP Tools

- `scan_site` - Scannt eine Website und analysiert die Struktur
- `crawl_links` - Crawlt alle Links einer Website
- `extract_model` - Extrahiert UI-Modell von einer Seite
- `generate_pom` - Generiert Page Object Model
- `generate_tests_full` - Komplette Pipeline: Crawl → POM → Tests
- `verify_pom` - Validiert ein POM
- `repair_file` - Repariert Syntax-Fehler

## 🎭 Beispiel-Workflow

```bash
# In Claude/VS Code mit MCP:
"Nutze andismcp und erstelle für https://example.com POMs und Tests"
```

Der Server führt automatisch aus:
1. Website crawlen
2. POMs generieren
3. TypeScript Tests erstellen
4. Playwright UI öffnen

---

## 📁 Projekt-Struktur

```
AndisMCP/
├── src/
│   ├── mcp_server.py       # MCP Server
│   ├── core/               # Core-Logik
│   └── tools/              # MCP Tools
├── tests/                  # Playwright Tests (TypeScript)
├── pages/                  # Page Object Models (TypeScript)
├── out/                    # Generierte Dateien (nicht im Repo)
├── .vscode/
│   └── mcp.json           # MCP-Konfiguration
├── package.json            # Node.js Dependencies
├── playwright.config.ts    # Playwright Config
├── requirements.txt        # Python Dependencies
└── .env                    # API Keys (nicht im Repo)
```

---

## 🤝 Zusammenarbeit

Wenn du an diesem Projekt mitarbeitest:

1. **Clone das Repo** (siehe Setup oben)
2. **Erstelle einen Branch** für deine Features
3. **Pushe deine Änderungen**
4. **Erstelle einen Pull Request**

Die `.vscode/mcp.json` nutzt relative Pfade - funktioniert auf jedem Rechner! 🚀

---

## 📝 Weitere Dokumentation

- 📋 [Requirements & Dependencies](REQUIREMENTS.md)
- 🔄 [Workflow Guide](WORKFLOW.md)
- ✨ [Features & Improvements](IMPROVEMENTS.md)

---

**Made with 🎭 by Andreas using MCP & Playwright**
