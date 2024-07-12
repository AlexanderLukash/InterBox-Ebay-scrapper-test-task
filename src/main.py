import json

from src.app.scrapper import EbayScraper
from src.app.utils import save_data

if __name__ == "__main__":
    url = str(input("Enter your url:> "))
    scraper = EbayScraper(url)
    scraper.fetch_data()
    data = scraper.get_data()
    print(json.dumps(data, indent=4))
    save_data(data, "../data/scraped_data.json")
