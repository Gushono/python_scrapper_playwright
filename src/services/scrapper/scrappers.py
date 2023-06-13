import random
import time
from abc import ABC
from enum import Enum

from playwright.async_api import async_playwright, Page

from src.dtos.dtos import CompanyDetails, CompanyPercentageStarReviews


class G2CrowdUrls(Enum):
    MainPage = "https://www.g2.com"


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'


class ScraperBase(ABC):
    async def scrape(self, url):
        pass

    @staticmethod
    async def scrape_description(page: Page) -> str:
        try:
            header_description_element = await page.query_selector('div.l5')
            header_description = await header_description_element.inner_text()

            paragraph_description_element = await page.query_selector('div.ws-pw > p')
            paragraph_description = await paragraph_description_element.inner_text()

            return f"{header_description}\n\n {paragraph_description}"

        except Exception as ex:
            print(ex)
            return ""

    @staticmethod
    async def scrape_rating(page: Page) -> str:
        review_count_element = await page.query_selector('h3.l2')
        review_count_text = await review_count_element.inner_text()

        rating_element = await page.query_selector('.fw-semibold')
        rating_stars = await rating_element.inner_text()

        return f"{review_count_text} \n\n ({rating_stars.rstrip()}) out of 5 stars"

    @staticmethod
    async def scrape_percentage_of_all_star_reviews(page: Page) -> list[CompanyPercentageStarReviews]:
        try:
            progress_elements = await page.query_selector_all('.progress-meter')
            star_ratings: list[CompanyPercentageStarReviews] = []

            for i, element in enumerate(progress_elements):
                style_value = await element.get_attribute('style')
                width_value = style_value.split(':')[1].strip(';').rstrip().lstrip()
                star_text = str(5 - i) + ' star'
                star_ratings.append(CompanyPercentageStarReviews(
                    star=star_text,
                    percentage=width_value
                ))

            return star_ratings
        except Exception as ex:
            print(ex)
            return []

    @staticmethod
    async def scrape_printscreen(page: Page) -> str:
        try:
            path_to_screenshot = f"output/{random.randint(1, 1000)}.png"
            await page.screenshot(path=path_to_screenshot)
            return path_to_screenshot
        except Exception as ex:
            print(ex)
            return ""


class G2CrowdScraper(ScraperBase):
    async def scrape(self, url: str):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=False)
            context = await browser.new_context(user_agent=user_agent, java_script_enabled=True)
            page = await context.new_page()
            await page.goto(G2CrowdUrls.MainPage.value, wait_until='networkidle')

            await self.scrape_printscreen(page)
            await self.scroll_page_randomly(page)

            input_field = await page.query_selector('input[name="query"]')
            await input_field.fill(url)
            time.sleep(random.randint(1, 5))
            await input_field.press('Enter')
            await page.wait_for_load_state('networkidle')

            time.sleep(random.randint(1, 5))

            await self.scrape_printscreen(page)

            page_content = await page.content()
            print(page_content)

            product_title = await page.query_selector('div.product-listing__title.mb-1 a')

            if not product_title:
                await browser.close()
                return Exception(f"Product title not found for url: {url}")

            await product_title.click()
            await page.wait_for_load_state('networkidle')
            await self.scrape_printscreen(page)

            description = await self.scrape_description(page)
            rating = await self.scrape_rating(page)
            percentage_of_all_star_reviews = await self.scrape_percentage_of_all_star_reviews(page)

            await browser.close()

            return CompanyDetails(
                url=url,
                description=description,
                rating=rating,
                percentage_of_all_star_reviews=percentage_of_all_star_reviews
            )

    @staticmethod
    async def scroll_page_randomly(page):
        scroll_position = await page.evaluate('window.pageYOffset')
        await page.evaluate('window.scrollTo(0, Math.random() * document.body.scrollHeight)')
        await page.evaluate(f'window.scrollTo(0, {scroll_position})')
