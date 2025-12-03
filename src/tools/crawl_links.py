"""Tool zum Crawlen aller Links auf einer Website."""

from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def crawl_links(base_url: str) -> dict:
    """
    Crawlt alle Links von der Hauptseite einer Website.

    Args:
        base_url: Basis-URL von der aus gecrawlt wird

    Returns:
        dict mit Keys: base_url, links (Liste von absoluten URLs)
    """
    links = []

    # Starte Playwright Browser (headless = ohne sichtbares Fenster)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # Navigiere zur Seite und warte bis alle Netzwerk-Requests fertig sind
            await page.goto(base_url, wait_until="networkidle", timeout=30000)
            html = await page.content()

            # Parse HTML mit BeautifulSoup und extrahiere alle Links
            soup = BeautifulSoup(html, "html.parser")
            
            for link in soup.find_all("a", href=True):
                href = link.get("href")
                # Ignoriere Anker-Links (die mit # beginnen)
                if href and not href.startswith("#"):
                    # Konvertiere relative URLs in absolute URLs
                    absolute_url = urljoin(base_url, href)
                    
                    # Behalte nur Links von der gleichen Domain
                    parsed_base = urlparse(base_url)
                    parsed_link = urlparse(absolute_url)
                    
                    # Prüfe ob Domain übereinstimmt
                    if parsed_link.netloc == parsed_base.netloc:
                        # Vermeide Duplikate
                        if absolute_url not in links:
                            links.append(absolute_url)

            return {
                "base_url": base_url,
                "links": links,
            }
        finally:
            await page.close()
            await browser.close()
