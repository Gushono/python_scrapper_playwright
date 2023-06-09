from src.services.csv_reader.csv_reader import CSVReader
from src.services.scrapper.scrappers import G2CrowdScrapper
from src.services.scrapper.service import ScrapingService


async def scrape():
    csv_reader = CSVReader()
    urls = csv_reader.read_urls_from_csv("g2crowdurls.csv")

    scrapper = G2CrowdScrapper()
    service = ScrapingService(scraper=scrapper)
    company_details = await service.scrape_companies_from_urls(urls)

    return company_details
