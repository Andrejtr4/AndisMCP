"""Tool zum Extrahieren eines UI-Modells aus dem DOM mittels LLM."""

import json
import os
from typing import Optional, Dict, Any

from langchain_openai import ChatOpenAI
from src.core.prompts import EXTRACT_INSTRUCTIONS


def extract_model(url: str, dom: str, hints: Optional[str] = None) -> Dict[str, Any]:
    """
    Extrahiert ein PageModel aus dem DOM mithilfe eines LLM (KI).
    
    Args:
        url: URL der Seite
        dom: HTML/DOM-Inhalt der Seite
        hints: Optionale Hinweise für die KI
    
    Returns:
        Dict mit UI-Elementen und deren Locators
    """
    # Hole API-Key aus Umgebungsvariablen
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")

    # Initialisiere OpenAI LLM (GPT-4o-mini)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, api_key=api_key)

    # Kürze DOM falls zu lang (Token-Limit)
    if len(dom) > 5000:
        dom = dom[:5000]

    # Baue Prompt für die KI
    prompt = f"""{EXTRACT_INSTRUCTIONS}

URL: {url}
DOM: {dom}
{f"Hints: {hints}" if hints else ""}

Return JSON with:
- "url": URL
- "elements": array with:
  - "name": camelCase name
  - "purpose": description
  - "locator": {{"strategy": "role/label/css", "value": "..."}}
  - "actions": ["click", "fill", ...] (optional)

Return ONLY JSON, no markdown."""

    # Rufe LLM auf und hole Antwort
    response = llm.invoke(prompt)
    content = response.content.strip()

    # Entferne Markdown-Code-Blöcke falls vorhanden
    if content.startswith("```"):
        content = content[content.find("{"):content.rfind("}") + 1]

    # Parse JSON-Antwort
    try:
        return json.loads(content)
    except Exception as e:
        raise ValueError(f"Parse error: {e}")
