# Web Scraping App

This is a Python application for web scraping company details from G2Crowd using Playwright and FastAPI.

## Description

The web scraping app allows you to provide a CSV file containing G2Crowd URLs of companies. It uses the Playwright
library to scrape the contents of each company's page and extract the desired information. The scraped data is then
returned in a structured format (JSON) with fields and values.

The app is built using FastAPI, which provides a web-based user interface to interact with the scraping functionality.

## Prerequisites

- Python 3.10 or higher
- Poetry (dependency management)

## Installation

1. Clone the repository:

   ```bash
   $ git clone https://github.com/Gushono/python_scrapper_playwright
   $ cd python_scrapper_playwright

    ```

2. Install the dependencies using Poetry:

   ```bash
    $ poetry install

   ```

## Usage

1. Prepare a CSV file containing the G2Crowd URLs of the companies you want to scrape.
   Make sure the file is named g2crowdurls.csv and placed in the root directory of the project.

   Example CSV file (g2crowdurls.csv):

   url
   https://www.g2crowd.com/companyA
   https://www.g2crowd.com/companyB

2. Start the FastAPI server:

   ```
   $ poetry run uvicorn app:app 
   ```

   The server will start running on http://localhost:8000.

3. Make a get request to /v1/scrape and you gonna receive the results.

## Usage with makefile and docker

1. You can run a command to see all available commands:

   ```
   $ make help
   ```

2. You can run a command to execute all steps of docker and run you app

   ```
   $ make start
   ```
   

## Documentation
1. You can access the documentation of the API by going to http://localhost:8000/docs.

## Possible Improvements
#### 1. Queueing and Separating Processing: Currently, the scraping process runs in a single execution flow, where URLs are scraped one after another. To improve efficiency and scalability, you can consider implementing a queue-based system. This approach involves pushing URLs into a queue and having separate worker processes or threads to consume URLs from the queue and perform scraping asynchronously. This can help parallelize the scraping process and handle a large number of URLs more efficiently.

#### 2. Error Handling and Retry Mechanism: Enhance the error handling mechanism to handle exceptions gracefully during the scraping process. Implement a retry mechanism for failed requests or intermittent errors to increase the chances of successful scraping. You can also implement logging to capture and analyze errors for debugging and monitoring purposes.

#### 3. Unit Tests and Test Coverage: Enhance the test suite by adding more unit tests to cover different scenarios and edge cases. Ensure sufficient test coverage to validate the functionality of the scraping service and its components. This can help catch bugs and regressions early in the development process.
