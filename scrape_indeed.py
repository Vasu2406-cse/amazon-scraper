import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape Indeed
def scrape_indeed(search_query, location, num_pages=1):
    base_url = "https://www.indeed.com"
    job_data = []

    for page in range(num_pages):
        url = f"{base_url}/jobs?q={search_query.replace(' ', '+')}&l={location.replace(' ', '+')}&start={page * 10}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to retrieve page {page + 1}. Status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("div", class_="job_seen_beacon")

        for job in jobs:
            title = job.find("h2", class_="jobTitle").text.strip()
            company = job.find("span", class_="companyName").text.strip()
            location = job.find("div", class_="companyLocation").text.strip()
            summary = job.find("div", class_="job-snippet").text.strip()
            link = base_url + job.find("a", class_="jcs-JobTitle")["href"]

            job_data.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Summary": summary,
                "Link": link
            })

    return job_data

# Function to save data to Excel
def save_to_excel(data, filename="indeed_jobs.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

# Main function
if __name__ == "__main__":
    search_query = input("Enter job title to search: ")
    location = input("Enter location: ")
    num_pages = int(input("Enter number of pages to scrape: "))

    print("Scraping Indeed...")
    jobs = scrape_indeed(search_query, location, num_pages)

    if jobs:
        save_to_excel(jobs)
        print("Scraping completed successfully!")
    else:
        print("No jobs found.")