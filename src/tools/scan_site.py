"""Tool zum Scannen einer Website und Extrahieren des DOM."""

from playwright.async_api import async_playwright


async def scan_site(url: str) -> dict:
    """
    Scannt eine URL mit Playwright und extrahiert das DOM.

    Args:
        url: Ziel-URL die gescannt werden soll

    Returns:
        dict mit Keys: url, dom (HTML-Inhalt der Seite)
    """
    # Starte Playwright Browser
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # Navigiere zur Seite und warte bis alle Netzwerk-Requests fertig sind
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Hole den kompletten HTML-Inhalt der Seite
            dom = await page.content()

            return {
                "url": url,
                "dom": dom,  # Das komplette HTML/DOM
            }
        finally:
            # Schließe Browser und Seite (auch bei Fehler)
            await page.close()
            await browser.close()
