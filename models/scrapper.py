import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from models.book import Book

BASE_URL = "https://books.toscrape.com/"
BASE_URL_BOOKS = "https://books.toscrape.com/catalogue/"

class Scrapper:
    
    def fetch_page(url):
        """Makes an HTTP request to retrieve the content of the page."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête : {e}")
            return None

    def extract_category_urls():
        """Extracts all category URLs from the page."""
        soup = Scrapper.fetch_page(BASE_URL)
        if not soup:
            return []

        category_urls = []
        categories = soup.select('.side_categories a')

        for link in categories:
            href = link.get('href')
            if href:
                full_url = urljoin(BASE_URL, href)
                if "catalogue/category/books_1/index.html" not in full_url:
                    category_urls.append(full_url)
                
        return category_urls
    
    def extract_book_urls(category_url):
        """Extracts all book URLs from a category page.
        Handles pagination if the number of results exceeds 20."""
        soup = Scrapper.fetch_page(category_url)
        if not soup:
            return []

        book_urls = []
        while True:
            books = soup.select('h3 a')
            for book in books:
                book_url = book['href'].replace('../../../', '')
                book_urls.append(urljoin(BASE_URL_BOOKS, book_url))

            # Vérifier s'il y a une page suivante
            next_page = soup.select_one('.next a')
            if next_page:
                next_page_url = urljoin(category_url, next_page['href'])
                soup = Scrapper.fetch_page(next_page_url)
            else:
                break

        return book_urls
    
    def extract_book_data(book_url):
        """Extracts product data from a book page."""
        soup = Scrapper.fetch_page(book_url)
        if not soup:
            return None

        title = soup.find("h1").text if soup.find("h1") else "Inconnu"
        category = soup.select("ul.breadcrumb li")[-2].text.strip()
        upc = soup.select_one("table tr:nth-of-type(1) td").text
        price_incl = soup.select_one("table tr:nth-of-type(4) td").text
        price_excl = soup.select_one("table tr:nth-of-type(3) td").text
        availability = soup.select_one("table tr:nth-of-type(6) td").text
        description = soup.select_one("#product_description + p").text if soup.select_one("#product_description + p") else "Pas de description"
        
        image_rel_url = soup.select_one(".item.active img")["src"]
        image_url = urljoin(BASE_URL, image_rel_url)

        rating_classes = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        review = rating_classes.get(soup.find("p", class_="star-rating")["class"][1], 0)

        return Book(book_url, upc, title, price_incl, price_excl, availability, description, category, review, image_url)
