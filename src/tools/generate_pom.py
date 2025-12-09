"""Tool zum Generieren von Page Object Models (POMs) aus UI-Modellen."""

import os
from pathlib import Path
from typing import Dict, Any
from src.core.prompts import IMPROVE_POM_PROMPT


def generate_pom(name: str, model: Dict[str, Any], use_ai: bool = True, llm=None) -> str:
    """
    Generiert eine Python POM-Klassen-Datei aus einem PageModel.
    Nutzt optional KI um POMs mit Best Practices zu verbessern.

    Args:
        name: Klassenname (z.B. 'MainPage')
        model: PageModel-Instanz mit UI-Elementen
        use_ai: KI zur Verbesserung des POMs nutzen (Standard: True)
        llm: LLM-Client aus der Pipeline (AzureChatOpenAI)

    Returns:
        Pfad zur generierten POM-Datei
    """
    # Erstelle Output-Verzeichnis für POMs
    poms_dir = Path("out/POMS")
    poms_dir.mkdir(parents=True, exist_ok=True)

    # Fallback falls kein Name angegeben
    if not name:
        name = "GeneratedPage"

    # Konvertiere Name in CamelCase Klassenname
    class_name = "".join(word.capitalize() for word in name.split("_"))
    
    # Generiere Basis-POM
    basic_pom = _generate_basic_pom(class_name, model)
    
    # Optional: Verbessere POM mit KI
    if use_ai:
        try:
            enhanced_pom = _enhance_pom_with_ai(basic_pom, class_name, model, llm)
        except Exception as e:
            print(f"AI enhancement failed, using basic POM: {e}")
            enhanced_pom = basic_pom
    else:
        enhanced_pom = basic_pom

    # Schreibe POM-Datei
    filename = f"{class_name}.py"
    file_path = poms_dir / filename
    file_path.write_text(enhanced_pom)

    return str(file_path)


def _generate_basic_pom(class_name: str, model: Dict[str, Any]) -> str:
    """Generiert ein Basis-POM-Template ohne KI-Verbesserung."""
    locator_inits = []
    elements = model.get("elements", []) if isinstance(model, dict) else model.elements
    
    for elem in elements:
        elem_name = elem.get("name") if isinstance(elem, dict) else elem.name
        locator = elem.get("locator") if isinstance(elem, dict) else elem.locator
        
        if isinstance(locator, dict):
            loc_code = _build_locator_code(locator.get("strategy"), locator.get("value"))
        else:
            loc_code = _build_locator_code(locator.strategy, locator.value)
        
        locator_inits.append(f"        self.{elem_name} = {loc_code}")

    locator_init_str = "\n".join(locator_inits)

    action_methods = []
    for elem in elements:
        elem_name = elem.get("name") if isinstance(elem, dict) else elem.name
        actions = elem.get("actions") if isinstance(elem, dict) else getattr(elem, "actions", None)
        
        if actions:
            for action in actions:
                method_code = _build_action_method(elem_name, action)
                action_methods.append(method_code)

    action_methods_str = "\n\n".join(action_methods) if action_methods else ""
    model_url = model.get("url") if isinstance(model, dict) else getattr(model, "url", "https://example.com")

    # Build final class
    pom_template = f"""\"\"\"Auto-generated Page Object Model for Playwright.\"\"\"

from playwright.sync_api import Page, expect


class {class_name}:
    \"\"\"Page Object for {model_url}\"\"\"

    def __init__(self, page: Page) -> None:
        \"\"\"Initialize page elements.\"\"\"
        self.page = page
{locator_init_str}

    def goto(self) -> None:
        \"\"\"Navigate to the page.\"\"\"
        self.page.goto("{model_url}")
{f"{action_methods_str}" if action_methods_str else ""}
"""
    return pom_template


def _enhance_pom_with_ai(basic_pom: str, class_name: str, model: Dict[str, Any], llm=None) -> str:
    """Use AI to enhance POM with best practices."""
    if llm is None:
        from src.core.pipeline import PlaywrightPipeline
        pipeline = PlaywrightPipeline()
        llm = pipeline.llm_gpt5
    
    prompt = IMPROVE_POM_PROMPT.format(current_pom=basic_pom)
    response = llm.invoke(prompt)
    improved_content = response.content.strip()
    
    if improved_content.startswith("```"):
        improved_content = improved_content[improved_content.find("import"):]
        if improved_content.endswith("```"):
            improved_content = improved_content[:improved_content.rfind("```")]
    
    return improved_content


def _build_locator_code(strategy: str, value: str) -> str:
    """Build Playwright locator code."""
    strategies = {
        "role": lambda v: f'self.page.get_by_role("{v}")',
        "label": lambda v: f'self.page.get_by_label("{v}")',
        "placeholder": lambda v: f'self.page.get_by_placeholder("{v}")',
        "testId": lambda v: f'self.page.get_by_test_id("{v}")',
        "text": lambda v: f'self.page.get_by_text("{v}")',
        "css": lambda v: f'self.page.locator("{v}")',
    }
    return strategies.get(strategy, lambda v: f'self.page.locator("{v}")')(value)


def _build_action_method(elem_name: str, action: str) -> str:
    """Build action method."""
    actions = {
        "click": (f"self.{elem_name}.click()", ""),
        "fill": (f"self.{elem_name}.fill(value)", "value: str"),
        "check": (f"self.{elem_name}.check()", ""),
    }
    code, param = actions.get(action, (f"# {action}", ""))
    return f"    def {action}_{elem_name}({param}) -> None:\n        {code}"
