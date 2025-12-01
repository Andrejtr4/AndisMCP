"""Node: generate Python Page Object Model class."""

from pathlib import Path
from typing import Dict, Any


def generate_pom(name: str, model: Dict[str, Any]) -> str:
    """
    Generate a Python POM class file from a PageModel.

    Args:
        name: Class name (e.g., 'MainPage')
        model: PageModel instance

    Returns:
        Path to generated POM file
    """
    poms_dir = Path("out/poms")
    poms_dir.mkdir(parents=True, exist_ok=True)

    # Generate class name if not provided
    if not name:
        name = "GeneratedPage"

    class_name = "".join(word.capitalize() for word in name.split("_"))

    # Build locator initialization code
    locator_inits = []
    elements = model.get("elements", []) if isinstance(model, dict) else model.elements
    
    for elem in elements:
        # Handle both dict and object formats
        elem_name = elem.get("name") if isinstance(elem, dict) else elem.name
        locator = elem.get("locator") if isinstance(elem, dict) else elem.locator
        
        if isinstance(locator, dict):
            loc_code = _build_locator_code(locator.get("strategy"), locator.get("value"))
        else:
            loc_code = _build_locator_code(locator.strategy, locator.value)
        
        locator_inits.append(f"        self.{elem_name} = {loc_code}")

    locator_init_str = "\n".join(locator_inits)

    # Build action helper methods (optional)
    action_methods = []
    for elem in elements:
        # Handle both dict and object formats
        elem_name = elem.get("name") if isinstance(elem, dict) else elem.name
        actions = elem.get("actions") if isinstance(elem, dict) else getattr(elem, "actions", None)
        
        if actions:
            for action in actions:
                method_code = _build_action_method(elem_name, action)
                action_methods.append(method_code)

    action_methods_str = "\n\n".join(action_methods) if action_methods else ""

    # Get URL from model
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

    # Save file
    filename = f"{class_name}.py"
    file_path = poms_dir / filename
    file_path.write_text(pom_template)

    return str(file_path)


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
