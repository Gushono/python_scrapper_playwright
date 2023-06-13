import asyncio
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
        try:
            review_count_element = await page.query_selector('h3.l2')
            review_count_text = await review_count_element.inner_text()

            rating_element = await page.query_selector('.fw-semibold')
            rating_stars = await rating_element.text_content()

            return f"{review_count_text} \n\n ({rating_stars.rstrip()}) out of 5 stars"
        except Exception as ex:
            print(ex)
            return ""

    @staticmethod
    async def scrape_percentage_of_all_star_reviews(page: Page) -> list[CompanyPercentageStarReviews]:
        try:
            progress_elements = await page.query_selector_all('.progress-meter.progress-meter--branding-rorange')
            star_ratings: list[CompanyPercentageStarReviews] = []

            for i, element in enumerate(progress_elements[0: 5]):
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

    @staticmethod
    async def scrape_obtain_reviews(page: Page) -> list[str]:
        try:
            div_element = await page.query_selector('div.f-1')
            div_content = await div_element.inner_text()

            h5_element = await page.query_selector('h5.l5')
            question_content = await h5_element.inner_text()

            print("Div Content:", div_content)
            print("Question Content:", question_content)
            return [div_content]
        except Exception as ex:
            print(ex)
            return []


async def simulate_mouse_movements(page):
    # Calculate the center point of the viewport
    viewport_center_x = 1280 // 2
    viewport_center_y = 720 // 2

    # Define the maximum distance to move the mouse from the center
    max_distance = 50

    # Simulate mouse movements
    for _ in range(5):  # Perform 5 movements
        # Calculate random offset values for the mouse movement
        offset_x = random.randint(-max_distance, max_distance)
        offset_y = random.randint(-max_distance, max_distance)

        # Calculate the target position based on the offset
        target_x = viewport_center_x + offset_x
        target_y = viewport_center_y + offset_y

        # Simulate mouse movement to the target position
        await page.mouse.move(target_x, target_y)

        # Wait for a random duration before the next movement
        await page.wait_for_timeout(random.randint(500, 1500))  # Wait for 0.5 to 1.5 seconds


class G2CrowdScraper(ScraperBase):

    async def scrape(self, url: str):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(channel="chrome", headless=False)
            context = await browser.new_context(
                user_agent=user_agent,
                java_script_enabled=True,
                bypass_csp=True,  # Bypass content security policy
                ignore_https_errors=True  # Ignore HTTPS errors
            )
            page = await context.new_page()

            # Configure request headers
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
            })

            await page.goto(G2CrowdUrls.MainPage.value, wait_until='networkidle')

            await self.scrape_printscreen(page)
            await self.scroll_page_randomly(page)

            input_field = await page.query_selector('input[name="query"]')
            await input_field.fill(url)
            await simulate_mouse_movements(page)
            time.sleep(1.2)
            await page.keyboard.press('Enter')

            await self.scrape_printscreen(page)

            page_content = await page.content()
            print(page_content)

            await self.scroll_page_randomly(page)
            product_title = await page.query_selector('div.product-listing__title.mb-1 a')

            if not product_title:
                await browser.close()
                return Exception(f"Product title not found for url: {url}")

            await simulate_mouse_movements(page)

            # Enable popup events
            context.on("page", lambda new_page: self.handle_new_page(new_page))

            # Click on the product title
            await page.click('div.product-listing__title.mb-1 a', force=True, button='middle')

            # Wait for the new page to be opened
            new_page = await self.wait_for_new_page()

            await page.close()
            await self.scrape_printscreen(new_page)

            description = await self.scrape_description(new_page)
            rating = await self.scrape_rating(new_page)
            percentage_of_all_star_reviews = await self.scrape_percentage_of_all_star_reviews(new_page)
            reviews = await self.scrape_obtain_reviews(new_page)

            await browser.close()

            return CompanyDetails(
                url=url,
                description=description,
                rating=rating,
                percentage_of_all_star_reviews=percentage_of_all_star_reviews
            )

    def handle_new_page(self, new_page: Page):
        # Store the new page for later use
        self.new_page = new_page

    async def wait_for_new_page(self):
        # Wait for the new page to be stored
        while not hasattr(self, 'new_page'):
            await asyncio.sleep(0.1)

        # Retrieve and return the new page
        new_page: Page = self.new_page

        time.sleep(2)

        delattr(self, 'new_page')
        return new_page

    @staticmethod
    async def scroll_page_randomly(page):
        scroll_position = await page.evaluate('window.pageYOffset')
        random_scroll_position = random.randint(0, 100)

        for i in range(1, 15):
            await page.evaluate(f'window.scrollBy(0, {random_scroll_position})')
            time.sleep(0.25)

        await page.evaluate(f'window.scrollTo(0, {scroll_position})')
