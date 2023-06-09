import random
from abc import ABC

from playwright.async_api import async_playwright, Page

from src.dtos.dtos import CompanyDetails


class ScraperBase(ABC):
    async def scrape(self, url):
        pass

    @staticmethod
    async def scrape_table_data(page: Page):
        try:
            table_data = await page.evaluate('''() => {
                       const table = document.querySelector('table');
                       const rows = Array.from(table.rows);

                       return rows.map(row => {
                           const cells = Array.from(row.cells);
                           return cells.map(cell => cell.innerText);
                       });
                   }''')

            return table_data
        except Exception as ex:
            print(ex)
            return None

    @staticmethod
    async def scrape_description(page):
        try:
            description_element = await page.query_selector('meta[name="description"]')
            description = await description_element.get_attribute('content')

            return description
        except Exception as ex:
            print(ex)
            return None

    @staticmethod
    async def scrape_links(page: Page):
        try:
            links = await page.evaluate('''() => {
                               const linkElements = Array.from(document.querySelectorAll('a'));
                               return linkElements.map(link => link.href);
                           }''')
            return links
        except Exception as ex:
            print(ex)
            return None


class G2CrowdScrapper(ScraperBase):
    async def scrape(self, url: str) -> CompanyDetails:
        async with async_playwright() as playwright:
            uuid = random.randint(1, 1000)

            browser = await playwright.chromium.launch()
            page = await browser.new_page()

            await page.goto(url)
            await page.wait_for_load_state('networkidle')

            title = await page.title()
            description = await self.scrape_description(page)
            links = await self.scrape_links(page)
            table_data = await self.scrape_table_data(page)
            path_to_screenshot = f"{uuid}.png"
            await page.screenshot(path=f"output/{path_to_screenshot}")

            await browser.close()

            return CompanyDetails(
                title=title,
                description=description,
                url=url,
                links=links,
                table_data=table_data,
                path_to_screenshot=path_to_screenshot
            )
