# 📦 Dependencies & Requirements

## 🐍 Python Dependencies (pyproject.toml)

### Core Framework
- `langgraph>=0.2.0` - Workflow orchestration
- `langchain-core>=0.3.0` - LangChain core functionality
- `langchain-openai>=0.2.0` - OpenAI integration

### Testing & Automation
- `playwright>=1.48` - Browser automation
- `pytest>=8.0` - Testing framework (für POM validation)

### MCP & API
- `modelcontextprotocol>=0.1.0` - MCP Server protocol
- `python-dotenv>=1.0.0` - Environment variable management

### Utilities
- `pydantic>=2.8` - Data validation
- `beautifulsoup4>=4.12.0` - HTML parsing

### Installation
```bash
pip install -e .
```

---

## 📦 TypeScript/Node Dependencies (out/package.json)

### Testing Framework
- `@playwright/test: ^1.40.0` - Playwright Test framework
- `typescript: ^5.0.0` - TypeScript compiler
- `@types/node: ^20.0.0` - Node.js type definitions

### Installation
```bash
cd out
npm install
npx playwright install
```

---

## 🔑 Environment Variables (.env)

**Required:**
```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
```

**Optional:**
```bash
# OpenAI Model (default: gpt-4o)
OPENAI_MODEL=gpt-4o

# Temperature (default: 0.1)
OPENAI_TEMPERATURE=0.1
```

---

## 🛠️ System Requirements

### Required
- **Python**: >= 3.10
- **Node.js**: >= 18.0 (für Playwright TypeScript Tests)
- **npm**: >= 8.0
- **OpenAI API Key**: Für AI-Test-Generierung

### Optional
- **Git**: Für Version Control
- **VS Code**: Für MCP Integration

---

## 📋 Installation Guide

### 1. Python Setup
```bash
# Virtual Environment erstellen
python -m venv venv

# Aktivieren
source venv/bin/activate  # macOS/Linux
# oder: venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -e .

# Playwright Browser installieren
playwright install chromium
```

### 2. TypeScript/Playwright Setup
```bash
# In out/ Verzeichnis
cd out

# Dependencies installieren
npm install

# Playwright Browser installieren
npx playwright install
```

### 3. Environment Variables
```bash
# .env Datei erstellen
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### 4. Quick Setup (All-in-One)
```bash
# Setup-Script ausführen
./scripts/setup_all.sh
```

---

## 🔄 Update Commands

### Python Dependencies aktualisieren
```bash
pip install --upgrade -e .
```

### TypeScript Dependencies aktualisieren
```bash
cd out
npm update
```

### Playwright Browser aktualisieren
```bash
npx playwright install --force
```

---

## 🧪 Verify Installation

```bash
# Python Packages prüfen
pip list | grep -E "langgraph|langchain|playwright|pydantic"

# Node Packages prüfen
cd out && npm list --depth=0

# Playwright Browser prüfen
npx playwright --version

# Environment prüfen
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('✅ OpenAI Key loaded' if os.getenv('OPENAI_API_KEY') else '❌ OpenAI Key missing')"
```

---

## 📦 Package Locations

```
DerBesteMCP/
├── pyproject.toml          # Python Dependencies
├── .env                    # Environment Variables
├── venv/                   # Python Virtual Environment
│
└── out/
    ├── package.json        # TypeScript Dependencies
    ├── package-lock.json   # Locked versions
    └── node_modules/       # Node packages
```

---

## 🚨 Common Issues

### "OPENAI_API_KEY not set"
```bash
# .env Datei prüfen
cat .env

# Neu erstellen
echo "OPENAI_API_KEY=sk-your-key" > .env
```

### "playwright not found"
```bash
# Playwright installieren
pip install playwright
playwright install chromium
```

### "npx: command not found"
```bash
# Node.js installieren
# macOS: brew install node
# Windows: Download von nodejs.org
```

### "Import Error: No module named..."
```bash
# Virtual Environment aktivieren
source venv/bin/activate

# Dependencies neu installieren
pip install -e .
```

---

## 💡 Development Dependencies

Falls du am Code entwickeln möchtest:

```bash
# Python Development
pip install black isort pylint mypy

# TypeScript Development
cd out
npm install -D eslint prettier
```

---

## 🎯 Minimal Requirements

**Nur für Test-Generierung:**
- Python >= 3.10
- OpenAI API Key
- `pip install -e .`

**Nur für Test-Ausführung:**
- Node.js >= 18
- `cd out && npm install`
- `npx playwright install`
