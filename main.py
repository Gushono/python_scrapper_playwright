import uvicorn
from fastapi import FastAPI

from csv_reader.csv_reader import CSVReader
from scrapper.scrappers import G2CrowdScrapper
from scrapper.service import ScrapingService

app = FastAPI()


@app.get("/scrape")
async def scrape():
    csv_reader = CSVReader()
    urls = csv_reader.read_urls_from_csv("input.csv")

    scrapper = G2CrowdScrapper()
    service = ScrapingService(scraper=scrapper)
    company_details = await service.scrape_companies_from_urls(urls)

    return company_details


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
