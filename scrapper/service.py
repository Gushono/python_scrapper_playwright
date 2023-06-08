import asyncio

from playwright.async_api import async_playwright

from scrapper.scrappers import ScraperBase, G2CrowdScrapper


class ScrapingService:
    def __init__(self, scraper: ScraperBase):
        self.scraper = scraper if scraper else G2CrowdScrapper()

    async def scrape_companies_from_urls(self, urls):
        tasks = [self.scrape_company_details(url) for url in urls]
        scraped_data = await asyncio.gather(*tasks)
        return scraped_data

    async def scrape_company_details(self, url: str):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(timeout=60000)
            page = await browser.new_page()
            page.set_default_timeout(60000)
            await page.goto(url)
            company_details = await self.scraper.scrape(page)
            await browser.close()

            return company_details
