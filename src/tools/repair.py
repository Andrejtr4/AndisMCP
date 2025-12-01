"""Node: repair Python code using LLM."""

import os
from pathlib import Path
from langchain_openai import ChatOpenAI


def repair_file(file_path: str, error_message: str = "") -> str:
    """Repair Python file using LLM."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")

    file_obj = Path(file_path)
    if not file_obj.exists():
        raise FileNotFoundError(f"Not found: {file_path}")

    current_content = file_obj.read_text()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0, api_key=api_key)

    prompt = f"""Fix this Python code:

{current_content}

Error: {error_message}

Return ONLY corrected Python code, no markdown."""

    response = llm.invoke(prompt)
    repaired = response.content.strip()

    # Clean markdown
    if repaired.startswith("```"):
        repaired = repaired[repaired.find("\n")+1:]
    if repaired.endswith("```"):
        repaired = repaired[:repaired.rfind("```")]

    file_obj.write_text(repaired.strip())
    return repaired
