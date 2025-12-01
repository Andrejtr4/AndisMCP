"""Node: extract PageModel from DOM using LLM."""

import json
import os
from typing import Optional, Dict, Any

from langchain_openai import ChatOpenAI
from src.core.prompts import EXTRACT_INSTRUCTIONS


def extract_model(url: str, dom: str, hints: Optional[str] = None) -> Dict[str, Any]:
    """Extract a PageModel from DOM using LLM."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, api_key=api_key)

    # Truncate DOM if too long
    if len(dom) > 5000:
        dom = dom[:5000]

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

    response = llm.invoke(prompt)
    content = response.content.strip()

    # Clean markdown
    if content.startswith("```"):
        content = content[content.find("{"):content.rfind("}") + 1]

    try:
        return json.loads(content)
    except Exception as e:
        raise ValueError(f"Parse error: {e}")
