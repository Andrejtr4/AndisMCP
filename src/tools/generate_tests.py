"""Node: generate pytest tests."""

from pathlib import Path


def generate_tests(pom_path: str, stories: str = "") -> str:
    """
    Generate pytest tests for a POM file.

    Args:
        pom_path: Path to POM file (e.g., 'out/poms/MainPage.py')
        stories: User stories or test hints

    Returns:
        Path to generated test file
    """
    tests_dir = Path("out/tests")
    tests_dir.mkdir(parents=True, exist_ok=True)

    pom_file = Path(pom_path)
    class_name = pom_file.stem

    # Extract import info
    import_name = class_name

    # Build test
    test_template = f'''"""Tests for {class_name}."""
import pytest
from playwright.sync_api import Page, sync_playwright


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()


def test_{class_name.lower()}_basic(page: Page):
    from out.poms.{class_name} import {class_name}
    pom = {class_name}(page)
    pom.goto()
    assert pom.page is not None

{f"# {stories}" if stories else ""}
'''

    # Save test file
    filename = f"test_{class_name.lower()}.py"
    file_path = tests_dir / filename
    file_path.write_text(test_template)

    return str(file_path)
