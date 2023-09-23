#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import json

# Define a function to scrape data from a single URL using BeautifulSoup
def scrape_data_with_bs4(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            product_title = soup.find('span', {'id': 'productTitle'}).get_text(strip=True)
            product_image_url = soup.find('img', {'id': 'landingImage'})['data-old-hires']
            price = soup.find('span', {'id': 'priceblock_ourprice'}).get_text(strip=True)
            
            product_details = []
            product_details_section = soup.find('div', {'id': 'productDescription'})
            
            if product_details_section:
                product_details = [p.get_text(strip=True) for p in product_details_section.find_all('p')]
            
            return {
                'Product Title': product_title,
                'Product Image URL': product_image_url,
                'Price': price,
                'Product Details': ' '.join(product_details)
            }
        elif response.status_code == 404:
            print(f"{url} not available (Error 404). Skipping...")
            return None
        else:
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while scraping {url}: {str(e)}")
        return None

# Initialize the driver outside of the try block
def scrape_data_with_selenium(url):
    driver = None  # Initialize driver as None
    try:
        chrome_service = ChromeService(executable_path='/path/to/chromedriver')
        driver = webdriver.Chrome(service=chrome_service)
        driver.get(url)

        product_title = driver.find_element_by_id('productTitle').text.strip()
        product_image_url = driver.find_element_by_id('landingImage').get_attribute('src')
        price = driver.find_element_by_id('priceblock_ourprice').text.strip()

        product_details = driver.find_element_by_id('productDescription').text.strip()

        return {
            'Product Title': product_title,
            'Product Image URL': product_image_url,
            'Price': price,
            'Product Details': product_details
        }

    except Exception as e:
        print(f"An error occurred while scraping {url}: {str(e)}")
        return None
    finally:
        if driver:
            driver.quit()  # Quit the driver if it was successfully initialized

# Read the CSV file with URLs
with open('sheet.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    urls = [f"https://www.amazon.{row['country']}/dp/{row['Asin']}" for row in csv_reader]

# Batch processing (100 URLs at a time)
batch_size = 100
for i in range(0, len(urls), batch_size):
    batch_urls = urls[i:i + batch_size]
    scraped_data = []
    
    start_time = time.time()
    
    for url in batch_urls:
        # Use BeautifulSoup for scraping
        data = scrape_data_with_bs4(url)
        
        # If BeautifulSoup fails, use Selenium
        if data is None:
            data = scrape_data_with_selenium(url)
        
        if data:
            scraped_data.append(data)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Save scraped data as JSON
    with open(f'output_batch_{i // batch_size}.json', 'w') as json_file:
        json.dump(scraped_data, json_file, indent=4)
    
    print(f"Batch {i // batch_size + 1} completed in {elapsed_time} seconds.")

print("All batches completed. Task finished.")

