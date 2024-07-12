from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup


class BaseScraper(ABC):
    def __init__(self, url):
        self.url = url
        self.data = {}

    @abstractmethod
    def fetch_data(self): ...

    @abstractmethod
    def parse_data(self, soup): ...

    @abstractmethod
    def get_data(self): ...


class EbayScraper(BaseScraper):
    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            self.parse_data(soup)
        else:
            print(
                f"Failed to retrieve the webpage. Status code: {response.status_code}",
            )

    def parse_data(self, soup):
        # Перевірка на None та правильні селектори
        title_elem = soup.find("h1", {"class": "x-item-title__mainTitle"})
        if title_elem:
            self.data["title"] = title_elem.get_text(strip=True)
        else:
            self.data["title"] = None

        self.data["link"] = self.url

        image_divs = soup.find_all("div", {"class": "ux-image-carousel-item"})
        if image_divs:
            unique_images = set()
            for div in image_divs:
                image_elems = div.find_all("img")
                for img in image_elems:
                    if "data-zoom-src" in img.attrs:
                        unique_images.add(img["data-zoom-src"])

            self.data["images"] = list(unique_images)
        else:
            self.data["images"] = []

        price_elem = soup.find("div", {"class": "x-price-primary"})
        if price_elem:
            self.data["price"] = price_elem.get_text(strip=True)
        else:
            self.data["price"] = None

        seller_elem = soup.find(
            "div",
            {"class": "x-sellercard-atf__info__about-seller"},
        )
        if seller_elem:
            self.data["seller"] = seller_elem.get_text(strip=True)
        else:
            self.data["seller"] = None

        seller_link_elem = soup.find(
            "div",
            {"class": "x-sellercard-atf__info__about-seller"},
        )
        if seller_link_elem:
            seller_link = seller_link_elem.find_all("a")
            if seller_link:
                self.data["seller_link"] = seller_link[0]["href"]
        else:
            self.data["seller"] = None

    def get_data(self):
        return self.data
