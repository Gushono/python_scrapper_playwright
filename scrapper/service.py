import asyncio

from dtos import CompanyDetails
from scrapper.scrappers import ScraperBase, G2CrowdScrapper


class ScrapingService:
    def __init__(self, scraper: ScraperBase):
        self.scraper = scraper if scraper else G2CrowdScrapper()

    async def scrape_companies_from_urls(self, urls: list[str]) -> list[CompanyDetails]:
        tasks = [self.scraper.scrape(url) for url in urls]
        scraped_data = await asyncio.gather(*tasks)

        results = []
        for data in scraped_data:
            if isinstance(data, Exception):
                print(f"Error occurred during scraping: {data}")
            elif isinstance(data, CompanyDetails):
                results.append(data)
            else:
                print(f"Unknown data type: {data}")

        return results
