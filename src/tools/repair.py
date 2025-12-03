"""Tool zur automatischen Reparatur von Python-Code mittels LLM."""

import os
from pathlib import Path
from langchain_openai import ChatOpenAI


def repair_file(file_path: str, error_message: str = "") -> str:
    """
    Repariert eine Python-Datei automatisch mithilfe eines LLM (KI).
    
    Args:
        file_path: Pfad zur zu reparierenden Datei
        error_message: Optionale Fehlermeldung zur besseren Reparatur
    
    Returns:
        Der reparierte Code als String
    """
    # Hole API-Key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")

    # Prüfe ob Datei existiert
    file_obj = Path(file_path)
    if not file_obj.exists():
        raise FileNotFoundError(f"Not found: {file_path}")

    # Lese aktuellen (fehlerhaften) Inhalt
    current_content = file_obj.read_text()
    
    # Initialisiere LLM mit temperature=0 für deterministische Ergebnisse
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0, api_key=api_key)

    # Baue Reparatur-Prompt
    prompt = f"""Fix this Python code:

{current_content}

Error: {error_message}

Return ONLY corrected Python code, no markdown."""

    # Rufe LLM auf
    response = llm.invoke(prompt)
    repaired = response.content.strip()

    # Entferne Markdown-Code-Blöcke falls vorhanden
    if repaired.startswith("```"):
        repaired = repaired[repaired.find("\n")+1:]
    if repaired.endswith("```"):
        repaired = repaired[:repaired.rfind("```")]

    # Schreibe reparierten Code zurück in Datei
    file_obj.write_text(repaired.strip())
    return repaired
