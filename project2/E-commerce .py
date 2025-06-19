from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3
import time

def scrape_products(product, count):
    # Setup database
    conn = sqlite3.connect("data/scraped_data.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS products (name TEXT, source TEXT, price REAL, availability TEXT, link TEXT)")
    cursor.execute("DELETE FROM products") 
    conn.commit()

    # Web scraping logic
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # Scrape Amazon
    driver.get(f"https://www.amazon.com/s?k={product}")
    time.sleep(2)

    amazon_counter = 0
    while amazon_counter < count:
        try:
            names = driver.find_elements(By.CSS_SELECTOR, "span.a-text-normal")
            prices = driver.find_elements(By.CSS_SELECTOR, "span.a-price-whole")
            links = driver.find_elements(By.CSS_SELECTOR, "a.a-link-normal")
            for i in range(amazon_counter, min(amazon_counter + 30, count)):
                if i >= len(names):
                    break
                name = names[i].text
                price = prices[i].text.replace(",", "") 
                link = links[i].get_attribute("href")
                availability = "Available"
                cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?)", (name, "Amazon", price, availability, link))
                conn.commit()
            amazon_counter += 30
            # Scroll down to load more products
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        except Exception as e:
            print("Error scraping Amazon:", e)
            break

    # Scrape eBay 
    driver.get(f"https://www.ebay.com/sch/i.html?_nkw={product}")
    time.sleep(2)
    ebay_counter = 0
    while ebay_counter < count:
        try:
            names = driver.find_elements(By.CSS_SELECTOR, ".s-item__title")
            prices = driver.find_elements(By.CSS_SELECTOR, ".s-item__price")
            links = driver.find_elements(By.CSS_SELECTOR, ".s-item__link")
            for i in range(ebay_counter, min(ebay_counter + 30, count)):
                if i >= len(names):
                    break
                name = names[i].text
                price = prices[i].text.replace(",", "")
                link = links[i].get_attribute("href")
                availability = "Available"
                cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?)", (name, "eBay", price, availability, link))
                conn.commit()
            ebay_counter += 30
            # Scroll down to load more products
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        except Exception as e:
            print("Error scraping eBay:", e)
            break

    driver.quit()
    conn.close()