import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to scrape Indeed
def scrape_indeed(query, location, num_pages=1):
    base_url = "https://www.indeed.com"
    jobs = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for page in range(num_pages):
        url = f"{base_url}/jobs?q={query}&l={location}&start={page * 10}"
        
        try:
            # Make the request to Indeed
            response = requests.get(url, headers=headers)
            
            # Debugging output: check the status code and content if it fails
            if response.status_code != 200:
                print(f"Failed to retrieve page {page + 1}. Status Code: {response.status_code}")
                print("Response content:", response.text[:200])  # Print part of the response to debug
                continue  # Skip to the next page if this one fails

            # If status code is OK (200), parse the HTML
            soup = BeautifulSoup(response.text, "html.parser")

            # Find job cards on the page
            job_cards = soup.find_all("div", class_="job_seen_beacon")
            if not job_cards:
                print(f"No jobs found on page {page + 1}")
            
            for job_card in job_cards:
                title_tag = job_card.find("h2", class_="jobTitle")
                company_tag = job_card.find("span", class_="companyName")
                location_tag = job_card.find("div", class_="companyLocation")
                summary_tag = job_card.find("div", class_="job-snippet")
                link_tag = job_card.find("a")

                # Make sure tags exist before accessing text
                if title_tag and company_tag and location_tag and summary_tag and link_tag:
                    title = title_tag.text.strip()
                    company = company_tag.text.strip()
                    location = location_tag.text.strip()
                    summary = summary_tag.text.strip()
                    link = base_url + link_tag["href"]

                    jobs.append({
                        "Title": title,
                        "Company": company,
                        "Location": location,
                        "Summary": summary,
                        "Link": link
                    })

        except requests.exceptions.RequestException as e:
            print(f"Error while requesting page {page + 1}: {e}")
        
        # Adding delay to prevent overwhelming the server
        time.sleep(2)

    return jobs

# Function to save data to Excel
def save_to_excel(data, filename="indeed_jobs.xlsx"):
    if data:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No data to save.")

# Main function
if __name__ == "__main__":
    query = "Software Engineer"  # Job title to search for
    location = "New York"        # Location to search in
    num_pages = 2                # Number of pages to scrape

    print("Scraping Indeed...")
    jobs = scrape_indeed(query, location, num_pages)
    save_to_excel(jobs)
    print("Scraping completed!")
