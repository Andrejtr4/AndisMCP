"""Generate TypeScript Playwright tests with AI-powered scenarios."""

import os
import json
from pathlib import Path
from langchain_openai import ChatOpenAI
from src.core.prompts import GENERATE_TEST_PROMPT_TS, EXTRACT_TEST_SCENARIOS_PROMPT


def generate_tests_ts(pom_path: str, stories: str = "") -> str:
    """Generate comprehensive TypeScript Playwright tests using LLM."""
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    
    pom_file = Path(pom_path)
    class_name = pom_file.stem
    pom_content = pom_file.read_text()
    
    url = _extract_url_from_pom(pom_content)
    elements = _extract_elements_from_pom(pom_content)
    
    # NEW: Scan the actual page to get real page structure
    page_snapshot = _scan_page_with_playwright(url)
    
    scenarios = _generate_test_scenarios(url, elements, api_key)
    
    tests_content = _generate_test_code(
        class_name=class_name,
        url=url,
        elements=elements,
        scenarios=scenarios,
        user_stories=stories,
        page_snapshot=page_snapshot,
        api_key=api_key
    )
    
    tests_dir = Path("out/tests")
    tests_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"{class_name.lower()}.spec.ts"
    file_path = tests_dir / filename
    file_path.write_text(tests_content)
    
    return str(file_path)


def _generate_test_scenarios(url: str, elements: list, api_key: str) -> list:
    """Use LLM to identify test scenarios."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, api_key=api_key)
    
    # Detect page type
    page_type = _detect_page_type(url, elements)
    
    prompt = EXTRACT_TEST_SCENARIOS_PROMPT.format(
        url=url,
        page_type=page_type,
        elements=elements[:10]  # First 10 elements
    )
    
    response = llm.invoke(prompt)
    content = response.content.strip()
    
    if content.startswith("```"):
        content = content[content.find("{"):content.rfind("}") + 1]
    
    try:
        result = json.loads(content)
        return result.get("scenarios", [])
    except:
        return []


def _scan_page_with_playwright(url: str) -> dict:
    """Scan the actual page using Playwright to get real structure."""
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=10000)
            
            # Get page snapshot using accessibility tree
            snapshot = page.accessibility.snapshot()
            
            # Extract useful information
            page_info = {
                "title": page.title(),
                "url": page.url,
                "snapshot": snapshot,
                "buttons": _extract_elements_by_role(page, "button"),
                "links": _extract_elements_by_role(page, "link"),
                "headings": _extract_elements_by_role(page, "heading"),
                "textboxes": _extract_elements_by_role(page, "textbox"),
                "forms": page.locator("form").count()
            }
            
            browser.close()
            return page_info
    except Exception as e:
        print(f"Warning: Could not scan page with Playwright: {e}")
        return {"title": "", "url": url, "buttons": [], "links": [], "headings": [], "textboxes": [], "forms": 0}


def _extract_elements_by_role(page, role: str) -> list:
    """Extract elements by their ARIA role."""
    try:
        elements = []
        locator = page.get_by_role(role)
        count = locator.count()
        
        for i in range(min(count, 20)):  # Limit to 20 elements
            try:
                element = locator.nth(i)
                text = element.text_content() or element.get_attribute("aria-label") or ""
                if text:
                    elements.append(text.strip()[:100])  # Limit text length
            except:
                pass
        
        return elements
    except:
        return []


def _generate_test_code(class_name: str, url: str, elements: list, 
                        scenarios: list, user_stories: str, page_snapshot: dict, api_key: str) -> str:
    """Generate TypeScript test code using LLM."""
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1, api_key=api_key)
    
    user_stories_section = f"\n## User Stories\n{user_stories}" if user_stories else ""
    
    # NEW: Add page snapshot information to prompt
    page_context = f"""
## Real Page Structure (from Playwright scan)
- Page Title: {page_snapshot.get('title', 'Unknown')}
- Buttons found: {page_snapshot.get('buttons', [])}
- Links found: {page_snapshot.get('links', [])}
- Headings found: {page_snapshot.get('headings', [])}
- Text inputs found: {page_snapshot.get('textboxes', [])}
- Forms count: {page_snapshot.get('forms', 0)}
"""
    
    prompt = GENERATE_TEST_PROMPT_TS.format(
        page_name=class_name,
        elements=elements[:15],
        url=url,
        user_stories_section=user_stories_section,
        page_context=page_context
    )
    
    if scenarios:
        scenarios_text = "\n".join(
            f"- {s['name']}: {s.get('expected', '')}" 
            for s in scenarios[:5]
        )
        prompt += f"\n\n## Suggested Scenarios\n{scenarios_text}"
    
    response = llm.invoke(prompt)
    content = response.content.strip()
    
    if content.startswith("```"):
        # Remove code fences
        lines = content.split('\n')
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1].strip() == "```":
            lines = lines[:-1]
        content = '\n'.join(lines)
    
    return content


def _extract_url_from_pom(pom_content: str) -> str:
    """Extract URL from POM goto() method."""
    import re
    match = re.search(r'page\.goto\(["\'](.+?)["\']\)', pom_content)
    return match.group(1) if match else "https://example.com"


def _extract_elements_from_pom(pom_content: str) -> list:
    """Extract element names from POM."""
    import re
    elements = re.findall(r'self\.(\w+)\s*=\s*self\.page', pom_content)
    return elements


def _detect_page_type(url: str, elements: list) -> str:
    """Detect page type based on URL and elements."""
    url_lower = url.lower()
    elements_lower = [e.lower() for e in elements]
    
    if "login" in url_lower or any("login" in e or "password" in e for e in elements_lower):
        return "Login Page"
    elif "checkout" in url_lower or any("cart" in e or "checkout" in e for e in elements_lower):
        return "Checkout Page"
    elif "search" in url_lower or any("search" in e for e in elements_lower):
        return "Search Page"
    elif any("form" in e or "submit" in e for e in elements_lower):
        return "Form Page"
    else:
        return "Generic Page"
