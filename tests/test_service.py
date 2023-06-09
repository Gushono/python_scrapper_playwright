from unittest.mock import MagicMock, AsyncMock

import pytest

from src.services.scrapper.service import ScrapingService
from src.dtos.dtos import CompanyDetails


@pytest.mark.asyncio
async def test_scrape_companies_from_urls_success():
    # Create a mock scraper
    scraper_mock = MagicMock()

    # Create an instance of the ScrapingService with the mock scraper
    service = ScrapingService(scraper_mock)

    urls = ["https://example.com/companyA", "https://example.com/companyB"]

    service.get_scraped_data = AsyncMock(return_value=[
        CompanyDetails(name="Company A", url="https://example.com/companyA"),
        CompanyDetails(name="Company B", url="https://example.com/companyB")
    ])

    results = await service.scrape_companies_from_urls(urls)
    assert len(results) == 2
    assert isinstance(results[0], CompanyDetails)
    assert isinstance(results[1], CompanyDetails)
