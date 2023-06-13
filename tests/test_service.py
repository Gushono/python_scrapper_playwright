from unittest.mock import MagicMock, AsyncMock

import pytest
from playwright.async_api import async_playwright

from src.dtos.dtos import CompanyDetails, CompanyPercentageStarReviews
from src.services.scrapper.scrappers import G2CrowdScraper
from src.services.scrapper.service import ScrapingService


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


@pytest.mark.asyncio
async def test_extract_description():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        html = '''<div class="paper paper--nestable" data-poison-text="">
                    <div class="l5 pb-0">What is LinkedIn Job Search?</div>
                    <div class="overflow-scrollbar-auto max-h-40 x-max-height-expand-initialized"
                        data-max-height-expand-show-less-text="Show Less<svg xmlns=&quot;http://www.w3.org/2000/svg&quot; contain=&quot;paint&quot; buffered-rendering=&quot;static&quot; viewBox=&quot;0 0 10 10&quot; class=&quot;ml-half py-1/12 icon-chevron-thin nessy-only&quot; aria-hidden=&quot;true&quot; focusable=&quot;false&quot; role=&quot;presentation&quot;><path d=&quot;M10.001 8.015V3.957L5.017.915l-5.016 3v4l5-3z&quot;></path></svg>"
                        data-max-height-expand-show-more-text="Show More<svg xmlns=&quot;http://www.w3.org/2000/svg&quot; contain=&quot;paint&quot; buffered-rendering=&quot;static&quot; viewBox=&quot;0 0 10 10&quot; class=&quot;ml-half py-1/12 r-180 icon-chevron-thin nessy-only&quot; aria-hidden=&quot;true&quot; focusable=&quot;false&quot; role=&quot;presentation&quot;><path d=&quot;M10.001 8.015V3.957L5.017.915l-5.016 3v4l5-3z&quot;></path></svg>"
                        data-max-height-expand-theme="white" data-max-height-expand-type="show more height revealer"
                        ue="max-height-expand">
                        <div class="ws-pw" data-poison="" itemprop="description">
                            <p>LinkedIn Job Search is a tool that allows users to quickly find job opportunities with location-based search and get automatic recommendations and notifications based on job searches.</p>
                        </div>
                    </div>
                </div>'''

        await page.set_content(html)

        description = await G2CrowdScraper().scrape_description(page)
        assert description == """What is LinkedIn Job Search?

 LinkedIn Job Search is a tool that allows users to quickly find job opportunities with location-based search and get automatic recommendations and notifications based on job searches."""
        await browser.close()


@pytest.mark.asyncio
async def test_rating_extraction():
    html = """
    <div class="show-for-large my-1 flex ai-c jc-sb">
        <div>
            <h3 class="l2 mb-half">917 LinkedIn Job Search Reviews</h3>
            <div class="mb-0">
                <div class="d-f ai-c">
                    <div class="stars  stars-9"></div>
                    <span class="c-midnight-90 pl-4th">
                        <span class="fw-semibold">4.5 </span> out of <span class="fw-semibold"> 5</span>
                    </span>
                </div>
            </div>
        </div>
        <div class="review-widget x-review-widget-initialized" data-review-widget-product-id="22108" ue="review-widget">
            <script type="text/template;name=products/review_widget_template">
                "{{#value}}
                <span>Edit review</span>
                {{/value}}
                {{^value}}
                <span>Write a Review</span>
                {{/value}}"
            </script>
            <a class="js-log-click x-review-widget btn btn--rorange nocase js-log-click" rel="noindex,nofollow" data-event-options="{&quot;product_id&quot;:22108,&quot;product_uuid&quot;:&quot;a455085c-9a73-4e08-8c5a-efcc0e7fbd56&quot;,&quot;product&quot;:&quot;LinkedIn Job Search&quot;,&quot;vendor_id&quot;:345,&quot;product_type&quot;:&quot;Software&quot;,&quot;placement&quot;:&quot;/products/reviews&quot;,&quot;name&quot;:&quot;Event::SurveyResponses::Take::Click&quot;}" href="https://www.g2.com/products/linkedin-job-search/take_survey">
                <span>Write a Review</span>
            </a>
        </div>
    </div>
    """

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html)

        star_ratings = await G2CrowdScraper().scrape_rating(page)

        assert star_ratings == '917 LinkedIn Job Search Reviews \n\n (4.5) out of 5 stars'

        await browser.close()


@pytest.mark.asyncio
async def test_stars_extraction():
    html = """
    <fieldset class="callout-fieldset">
        <label class="c-midnight-80 radios__button m-0">
            <input class="m-0 js-log-click radios__input radios__input--emphasized-text" data-event-options="{&quot;product_id&quot;:22108,&quot;product_uuid&quot;:&quot;a455085c-9a73-4e08-8c5a-efcc0e7fbd56&quot;,&quot;product&quot;:&quot;LinkedIn Job Search&quot;,&quot;vendor_id&quot;:345,&quot;product_type&quot;:&quot;Software&quot;,&quot;type&quot;:&quot;nps_score&quot;,&quot;value&quot;:&quot;5 star&quot;,&quot;name&quot;:&quot;Event::Products::Filter&quot;}"
                type="radio" value="5" name="filters[nps_score]" id="filters_nps_score_5">
            <div class="radios__text text-small-normal fw-regular py-0 xl:pl-0">
                <div class="d-f ai-c mb-half filter-results-slider">
                    <div class="filter-results-slider__text">
                        <div class="ellipsis-dynamic-wrapper">
                            <div class="ellipsis">5 star</div>
                        </div>
                    </div>
                    <div class="f-7">
                        <div class="progress progress--light-gray progress--narrow my-0 progress--rounded overflow-hidden">
                            <div class="progress-meter progress-meter--branding-rorange" style="width: 73.17339149400219%;"></div>
                        </div>
                    </div>
                    <div class="f-3">
                        <div class="text-right">671</div>
                    </div>
                </div>
            </div>
        </label>
        <label class="c-midnight-80 radios__button m-0">
            <input class="m-0 js-log-click radios__input radios__input--emphasized-text" data-event-options="{&quot;product_id&quot;:22108,&quot;product_uuid&quot;:&quot;a455085c-9a73-4e08-8c5a-efcc0e7fbd56&quot;,&quot;product&quot;:&quot;LinkedIn Job Search&quot;,&quot;vendor_id&quot;:345,&quot;product_type&quot;:&quot;Software&quot;,&quot;type&quot;:&quot;nps_score&quot;,&quot;value&quot;:&quot;4 star&quot;,&quot;name&quot;:&quot;Event::Products::Filter&quot;}"
                type="radio" value="4" name="filters[nps_score]" id="filters_nps_score_4">
            <div class="radios__text text-small-normal fw-regular py-0 xl:pl-0">
                <div class="d-f ai-c mb-half filter-results-slider">
                    <div class="filter-results-slider__text">
                        <div class="ellipsis-dynamic-wrapper">
                            <div class="ellipsis">4 star</div>
                        </div>
                    </div>
                    <div class="f-7">
                        <div class="progress progress--light-gray progress--narrow my-0 progress--rounded overflow-hidden">
                            <div class="progress-meter progress-meter--branding-rorange" style="width: 21.374045801526716%;"></div>
                        </div>
                    </div>
                    <div class="f-3">
                        <div class="text-right">196</div>
                    </div>
                </div>
            </div>
        </label>
        <label class="c-midnight-80 radios__button m-0">
            <input class="m-0 js-log-click radios__input radios__input--emphasized-text" data-event-options="{&quot;product_id&quot;:22108,&quot;product_uuid&quot;:&quot;a455085c-9a73-4e08-8c5a-efcc0e7fbd56&quot;,&quot;product&quot;:&quot;LinkedIn Job Search&quot;,&quot;vendor_id&quot;:345,&quot;product_type&quot;:&quot;Software&quot;,&quot;type&quot;:&quot;nps_score&quot;,&quot;value&quot;:&quot;3 star&quot;,&quot;name&quot;:&quot;Event::Products::Filter&quot;}"
                type="radio" value="3" name="filters[nps_score]" id="filters_nps_score_3">
            <div class="radios__text text-small-normal fw-regular py-0 xl:pl-0">
                <div class="d-f ai-c mb-half filter-results-slider">
                    <div class="filter-results-slider__text">
                        <div class="ellipsis-dynamic-wrapper">
                            <div class="ellipsis">3 star</div>
                        </div>
                    </div>
                    <div class="f-7">
                        <div class="progress progress--light-gray progress--narrow my-0 progress--rounded overflow-hidden">
                            <div class="progress-meter progress-meter--branding-rorange" style="width: 4.471101417666303%;"></div>
                        </div>
                    </div>
                    <div class="f-3">
                        <div class="text-right">41</div>
                    </div>
                </div>
            </div>
        </label>
        <label class="c-midnight-80 radios__button m-0">
            <input class="m-0 js-log-click radios__input radios__input--emphasized-text" data-event-options="{&quot;product_id&quot;:22108,&quot;product_uuid&quot;:&quot;a455085c-9a73-4e08-8c5a-efcc0e7fbd56&quot;,&quot;product&quot;:&quot;LinkedIn Job Search&quot;,&quot;vendor_id&quot;:345,&quot;product_type&quot;:&quot;Software&quot;,&quot;type&quot;:&quot;nps_score&quot;,&quot;value&quot;:&quot;2 star&quot;,&quot;name&quot;:&quot;Event::Products::Filter&quot;}"
                type="radio" value="2" name="filters[nps_score]" id="filters_nps_score_2">
            <div class="radios__text text-small-normal fw-regular py-0 xl:pl-0">
                <div class="d-f ai-c mb-half filter-results-slider">
                    <div class="filter-results-slider__text">
                        <div class="ellipsis-dynamic-wrapper">
                            <div class="ellipsis">2 star</div>
                        </div>
                    </div>
                    <div class="f-7">
                        <div class="progress progress--light-gray progress--narrow my-0 progress--rounded overflow-hidden">
                            <div class="progress-meter progress-meter--branding-rorange" style="width: 0.5452562704471101%;"></div>
                        </div>
                    </div>
                    <div class="f-3">
                        <div class="text-right">5</div>
                    </div>
                </div>
            </div>
        </label>
        <label class="c-midnight-80 radios__button m-0">
            <input class="m-0 js-log-click radios__input radios__input--emphasized-text" data-event-options="{&quot;product_id&quot;:22108,&quot;product_uuid&quot;:&quot;a455085c-9a73-4e08-8c5a-efcc0e7fbd56&quot;,&quot;product&quot;:&quot;LinkedIn Job Search&quot;,&quot;vendor_id&quot;:345,&quot;product_type&quot;:&quot;Software&quot;,&quot;type&quot;:&quot;nps_score&quot;,&quot;value&quot;:&quot;1 star&quot;,&quot;name&quot;:&quot;Event::Products::Filter&quot;}"
                type="radio" value="1" name="filters[nps_score]" id="filters_nps_score_1">
            <div class="radios__text text-small-normal fw-regular py-0 xl:pl-0">
                <div class="d-f ai-c mb-half filter-results-slider">
                    <div class="filter-results-slider__text">
                        <div class="ellipsis-dynamic-wrapper">
                            <div class="ellipsis">1 star</div>
                        </div>
                    </div>
                    <div class="f-7">
                        <div class="progress progress--light-gray progress--narrow my-0 progress--rounded overflow-hidden">
                            <div class="progress-meter progress-meter--branding-rorange" style="width: 0.43620501635768816%;"></div>
                        </div>
                    </div>
                    <div class="f-3">
                        <div class="text-right">4</div>
                    </div>
                </div>
            </div>
        </label>
    </fieldset>
    """
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html)

        star_ratings = await G2CrowdScraper().scrape_percentage_of_all_star_reviews(page)

        assert star_ratings == [CompanyPercentageStarReviews(star='5 star', percentage='73.17339149400219%'),
                                CompanyPercentageStarReviews(star='4 star', percentage='21.374045801526716%'),
                                CompanyPercentageStarReviews(star='3 star', percentage='4.471101417666303%'),
                                CompanyPercentageStarReviews(star='2 star', percentage='0.5452562704471101%'),
                                CompanyPercentageStarReviews(star='1 star', percentage='0.43620501635768816%')]

        return star_ratings
