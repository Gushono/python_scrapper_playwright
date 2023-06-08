from abc import ABC

from playwright.async_api import Page
from pydantic import BaseModel


class CompanyDetails(BaseModel):
    name: str
    description: str


class ScraperBase(ABC):
    async def scrape(self, url):
        raise NotImplementedError


class G2CrowdScrapper(ScraperBase):
    async def scrape(self, page: Page) -> CompanyDetails:
        h1 = await page.inner_text("h1")

        print(h1)

        return CompanyDetails(name=h1, description="description")
