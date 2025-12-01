"""Node: crawl all links from the main page."""

from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def crawl_links(base_url: str) -> dict:
    """
    Crawl all links from a website's main page.

    Args:
        base_url: Base URL to start crawling from

    Returns:
        dict with keys: base_url, links (list of absolute URLs)
    """
    links = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(base_url, wait_until="networkidle", timeout=30000)
            html = await page.content()

            # Parse HTML and extract links
            soup = BeautifulSoup(html, "html.parser")
            
            for link in soup.find_all("a", href=True):
                href = link.get("href")
                if href and not href.startswith("#"):
                    # Convert relative URLs to absolute
                    absolute_url = urljoin(base_url, href)
                    
                    # Only keep links from the same domain
                    parsed_base = urlparse(base_url)
                    parsed_link = urlparse(absolute_url)
                    
                    if parsed_link.netloc == parsed_base.netloc:
                        if absolute_url not in links:
                            links.append(absolute_url)

            return {
                "base_url": base_url,
                "links": links,
            }
        finally:
            await page.close()
            await browser.close()
