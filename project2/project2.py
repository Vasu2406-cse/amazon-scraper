import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape Indeed
def scrape_indeed(query, location, num_pages=1):
    base_url = "https://www.indeed.com"
    jobs = []

    for page in range(num_pages):
        url = f"{base_url}/jobs?q={query}&l={location}&start={page * 10}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for job_card in soup.find_all("div", class_="job_seen_beacon"):
            title = job_card.find("h2", class_="jobTitle").text.strip()
            company = job_card.find("span", class_="companyName").text.strip()
            location = job_card.find("div", class_="companyLocation").text.strip()
            summary = job_card.find("div", class_="job-snippet").text.strip()
            link = base_url + job_card.find("a")["href"]

            jobs.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Summary": summary,
                "Link": link
            })

    return jobs

# Function to save data to Excel
def save_to_excel(data, filename="indeed_jobs.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

# Main function
if __name__ == "__main__":
    query = "Software Engineer"  # Job title to search for
    location = "New York"        # Location to search in
    num_pages = 2                # Number of pages to scrape

    print("Scraping Indeed...")
    jobs = scrape_indeed(query, location, num_pages)
    save_to_excel(jobs)
    print("Scraping completed!")