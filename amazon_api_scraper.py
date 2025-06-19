from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
    ]
    return random.choice(user_agents)

def scrape_amazon(search_query, max_pages=1, headless=True):
    
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('start-maximized')
    options.add_argument('--no-sandbox')
    if headless:
        options.add_argument('--headless')
    options.add_argument(f"user-agent={get_random_user_agent()}")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    products = []

    for page in range(1, max_pages + 1):
        url = f'https://www.amazon.com/s?k={search_query}&page={page}'
        driver.get(url)
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot"))
            )
        except Exception as e:
            print(f"Error loading page {page}: {e}")
            continue
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        for item in soup.find_all('div', {'data-component-type': 's-search-result'}):
            try:
                name = item.h2.text.strip()
                price = item.find('span', 'a-price-whole').text.strip() if item.find('span', 'a-price-whole') else 'N/A'
                rating = item.find('span', 'a-icon-alt').text.strip() if item.find('span', 'a-icon-alt') else 'N/A'
                reviews = item.find('span', {'class': 'a-size-base'}).text.strip() if item.find('span', {'class': 'a-size-base'}) else 'N/A'
                
            
                availability = 'Check Product Page'
                
                
                image_url = item.find('img', class_='s-image')['src'] if item.find('img', class_='s-image') else 'N/A'

                products.append({
                    'name': name,
                    'price': price,
                    'rating': rating,
                    'reviews': reviews,
                    'availability': availability,
                    'image_url': image_url
                })
            except Exception as e:
                print(f"Error extracting data from item: {e}")
                continue

    driver.quit()
    return products

if __name__ == "__main__":
    search_query = 'laptop'
    max_pages = 2  

    products = scrape_amazon(search_query, max_pages=max_pages, headless=True)

    if products:
        df = pd.DataFrame(products)
        df.to_csv('amazon_products.csv', index=False)
        print('Data saved to amazon_products.csv')
    else:
        print("No data found to save.")
