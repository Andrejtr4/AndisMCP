"""Node: scan a website and extract DOM content."""

from playwright.async_api import async_playwright


async def scan_site(url: str) -> dict:
    """
    Scan a URL with Playwright and extract DOM.

    Args:
        url: Target URL

    Returns:
        dict with keys: url, dom
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            dom = await page.content()

            return {
                "url": url,
                "dom": dom,
            }
        finally:
            await page.close()
            await browser.close()
