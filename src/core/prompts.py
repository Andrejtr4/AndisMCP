"""Prompts for AI-powered code generation.

⚙️ ARCHITEKTUR (FEST KONFIGURIERT):
✅ POMs werden IMMER in Python generiert (out/POMS/*.py)
✅ Tests werden IMMER in TypeScript generiert (out/TESTS/*.spec.ts)
✅ Playwright UI öffnet automatisch nach der Generierung
"""

# POM Improvement Prompt
IMPROVE_POM_PROMPT = """You are an expert in Playwright Page Object Models. Improve this Python POM.

## ⚙️ ARCHITEKTUR (FEST KONFIGURIERT - NICHT ÄNDERBAR)
✅ **POMs werden IMMER in Python generiert** (out/POMS/*.py)
✅ **Tests werden IMMER in TypeScript generiert** (out/TESTS/*.spec.ts)
✅ **Playwright UI öffnet automatisch nach der Generierung**

Du verbesserst das Python Page Object Model. Tests werden später automatisch in TypeScript generiert.

## Current POM:
{current_pom}

## Improvement Guidelines:
1. **Better Locators**: Use role-based selectors where possible
2. **Helper Methods**: Add common actions (wait_for_visible, is_enabled, etc.)
3. **Explicit Waits**: Add proper waiting strategies
4. **Validation Helpers**: Add methods to check element states
5. **Documentation**: Add clear docstrings
6. **Type Hints**: Use proper Python type hints

## Keep:
- All existing elements and methods
- The class name and structure
- The goto() method with the URL

## Add:
- Helper methods for common operations
- Validation/assertion helpers
- Proper docstrings for all methods
- Type hints for parameters and return values

## Output Requirements:
Return ONLY Python code. NO markdown fences (```), NO explanations.
Start directly with the docstring and imports.
"""

# Element Extraction Prompt
EXTRACT_INSTRUCTIONS = """Extract interactive UI elements from this page.

## ⚙️ ARCHITEKTUR (FEST KONFIGURIERT - NICHT ÄNDERBAR)
✅ **POMs werden IMMER in Python generiert** (out/POMS/*.py)
✅ **Tests werden IMMER in TypeScript generiert** (out/TESTS/*.spec.ts)
✅ **Playwright UI öffnet automatisch nach der Generierung**

Du extrahierst UI-Elemente für Python Page Object Models.

## Extraction Rules:
1. Identify all interactive elements (buttons, links, inputs, forms)
2. Generate camelCase names for each element
3. Suggest the best Playwright locator strategy:
   - role: ARIA roles (button, link, textbox, heading, etc.) - PREFERRED
   - label: Form labels
   - placeholder: Input placeholders
   - testId: data-testid attributes
   - text: Visible text
   - css: CSS selectors (fallback)
4. List possible actions: click, fill, check, select, hover

## Return Format:
Return JSON with this structure:
{
  "url": "page url",
  "elements": [
    {
      "name": "elementName",
      "purpose": "What this element does",
      "locator": {
        "strategy": "role|label|css|etc",
        "value": "button|specific-value"
      },
      "actions": ["click", "fill", ...]
    }
  ]
}

Return ONLY JSON, no markdown, no explanations.
"""

# Test Scenario Extraction (imported from test_prompts_ts.py)
EXTRACT_TEST_SCENARIOS_PROMPT = """Analyze this page and identify key test scenarios.

## ⚙️ ARCHITEKTUR (FEST KONFIGURIERT - NICHT ÄNDERBAR)
✅ **POMs werden IMMER in Python generiert** (out/POMS/*.py)
✅ **Tests werden IMMER in TypeScript generiert** (out/TESTS/*.spec.ts)
✅ **Playwright UI öffnet automatisch nach der Generierung**

URL: {url}
Page Type: {page_type}
Elements: {elements}

Generate scenarios based on the page type and elements. Return JSON only:

{{
  "scenarios": [
    {{
      "name": "scenario_name",
      "type": "happy_path|validation|edge_case|navigation|accessibility",
      "expected": "expected outcome"
    }}
  ]
}}

Return ONLY the JSON, no additional text.
"""

# TypeScript Test Generation (imported from test_prompts_ts.py)
GENERATE_TEST_PROMPT_TS = """You are an expert Playwright test engineer. Generate comprehensive TypeScript tests.

## ⚙️ ARCHITEKTUR (FEST KONFIGURIERT - NICHT ÄNDERBAR)
✅ **POMs werden IMMER in Python generiert** (out/POMS/*.py)
✅ **Tests werden IMMER in TypeScript generiert** (out/TESTS/*.spec.ts)
✅ **Playwright UI öffnet automatisch nach der Generierung**

Du generierst NUR TypeScript/Playwright Tests. Die POMs sind bereits in Python vorhanden.

## Context
- Page: {page_name}
- Available elements: {elements}
- URL: {url}
{user_stories_section}
{page_context}

## CRITICAL RULES - READ CAREFULLY
1. **ONLY test elements that actually exist on the page** (see "Real Page Structure" above)
2. **Use the EXACT element names** from the "Real Page Structure" section
3. **Use proper Playwright selectors**: page.getByRole(), page.getByText(), page.locator()
4. **DO NOT assume elements exist** - only use what you see in the page structure
5. **DO NOT test forms if forms count is 0**
6. **DO NOT test validation if no form inputs exist**
7. **Keep tests simple and realistic** based on what the page actually does

## Test Requirements
1. Coverage: Test all critical user flows
2. Assertions: Use expect() for proper waiting and assertions
3. Naming: Descriptive test names (test('should login with valid credentials'))
4. Isolation: Each test should be independent
5. Best Practices:
   - Wait for elements before interaction
   - Use proper selectors (role > label > test-id > css)
   - Add error scenarios
   - Test responsive behavior if applicable

## Test Generation Strategy

ANALYZE the "Real Page Structure" above and create 3-5 realistic tests based on what actually exists:

### Test Type Selection Rules:

**IF page has forms/inputs (forms > 0 or textboxes exist):**
1. Test filling and submitting the form
2. Test validation (if applicable)
3. Test clearing/resetting form

**IF page has buttons:**
1. Test clicking each major button
2. Test what happens after button click (new elements appear, navigation, etc.)
3. Test button states (enabled/disabled)

**IF page has links:**
1. Test that important links are visible
2. Test clicking links (verify navigation or new tab)
3. Test link attributes (href, target)

**IF page has headings/text content:**
1. Test that expected headings are visible
2. Test that page title is correct
3. Test content rendering

**IF page has interactive elements (add/remove, show/hide):**
1. Test the interaction (click to add/remove)
2. Test counting elements before/after
3. Test multiple interactions

### Example Test Patterns:

**For a page with "Add Element" button:**
```typescript
test('should add element when button clicked', async ({{ page }}) => {{
  await page.goto('{url}');
  
  // Verify no elements initially
  await expect(page.getByRole('button', {{ name: 'Delete' }})).toHaveCount(0);
  
  // Click add button
  await page.getByRole('button', {{ name: 'Add Element' }}).click();
  
  // Verify element was added
  await expect(page.getByRole('button', {{ name: 'Delete' }})).toHaveCount(1);
}});
```

**For a page with heading and links:**
```typescript
test('should display correct heading', async ({{ page }}) => {{
  await page.goto('{url}');
  
  // Check heading exists (use EXACT text from "Real Page Structure")
  await expect(page.getByRole('heading', {{ name: 'Exact Heading Text' }})).toBeVisible();
}});

test('should have working link', async ({{ page }}) => {{
  await page.goto('{url}');
  
  // Check link exists
  const link = page.getByRole('link', {{ name: 'Link Text' }});
  await expect(link).toBeVisible();
  await expect(link).toHaveAttribute('href', 'expected-url');
}});
```

**For a login form:**
```typescript
test('should login with valid credentials', async ({{ page }}) => {{
  await page.goto('{url}');
  
  // Fill form (use exact input names from page structure)
  await page.getByRole('textbox', {{ name: 'username' }}).fill('tomsmith');
  await page.getByRole('textbox', {{ name: 'password' }}).fill('SuperSecretPassword!');
  
  // Submit
  await page.getByRole('button', {{ name: 'Login' }}).click();
  
  // Verify success
  await expect(page.getByText('You logged into a secure area')).toBeVisible();
}});
```

## Output Requirements

Generate 3-5 realistic tests based on the actual page structure. Each test should:

1. **Use EXACT element names** from "Real Page Structure"
2. **Use proper Playwright selectors**: 
   - `page.getByRole('button', {{ name: 'Button Text' }})`
   - `page.getByRole('link', {{ name: 'Link Text' }})`
   - `page.getByRole('heading', {{ name: 'Heading Text' }})`
   - `page.getByRole('textbox', {{ name: 'Input Label' }})`
3. **Test only what exists** - don't make assumptions
4. **Be specific** - use exact text from the page
5. **Follow realistic user flows** - what would a real user do?

## Output Format
Return ONLY TypeScript code. NO markdown fences (```), NO explanations, NO additional text.

Start directly with:
import {{ test, expect }} from '@playwright/test';

test.describe('{page_name} Page', () => {{
  // Your tests here
}});

CRITICAL: 
- NO ``` code fences
- NO explanatory text before or after code
- ONLY valid TypeScript code
- Use EXACT element text from "Real Page Structure"
- Create realistic tests based on what the page actually does
"""
