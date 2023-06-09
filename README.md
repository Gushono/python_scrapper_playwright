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
