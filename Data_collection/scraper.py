import requests
import pandas as pd

# OpenPhish provides a list of phishing URLs
URL = "https://openphish.com/feed.txt"

def fetch_openphish():
    response = requests.get(URL)
    
    if response.status_code == 200:
        phishing_sites = response.text.split("\n")  # Split URLs by line

        df = pd.DataFrame(phishing_sites, columns=["URL"])
        df.to_csv("phishing_data.csv", index=False)

        print(f"✅ Scraped {len(phishing_sites)} phishing URLs from OpenPhish!")
    else:
        print("❌ Failed to fetch phishing data. Check the URL or network connection.")

if __name__ == "__main__":
    fetch_openphish()