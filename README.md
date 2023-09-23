# Python-Task-for-Relu-Consultancy
# Amazon Web Scraper

This Python script allows you to scrape data from Amazon product pages using both BeautifulSoup (bs4) and Selenium. It can handle a large number of URLs provided in a CSV file.

## Prerequisites

Make sure you have the following libraries and tools installed:

- Python (latest version)
- BeautifulSoup (`pip install beautifulsoup4`)
- Selenium (`pip install selenium`)
- ChromeDriver (download and set the path)

## Usage

1. Clone this repository to your local machine.
2. Create a virtual environment (optional but recommended).
3. Install the required libraries mentioned in the Prerequisites section.
4. Download ChromeDriver and set the path to the executable in the code.
5. Prepare your CSV file ('sheet.csv') with columns 'country' and 'Asin' for the Amazon URLs.
6. Run the `scraper.py` script:

7. The script will batch process the URLs, scrape the required data, and save the results in JSON files.

## Output

The scraped data will be saved in JSON files (e.g., `output_batch_0.json`, `output_batch_1.json`, etc.) in the same directory as the script. The JSON files contain a list of dictionaries, with each dictionary representing the scraped data for a product.
