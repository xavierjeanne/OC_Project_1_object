from models.scrapper import Scrapper
from views.exporter import Exporter

class Controller:
    def run(self):
        categories = Scrapper.extract_category_urls()
        
        for category_url in categories:
            print(f"Scraping de la catégorie : {category_url}")
            book_urls = Scrapper.extract_book_urls(category_url)
            books = []

            for book_url in book_urls:
                book = Scrapper.extract_book_data(book_url)
               
                if book:
                    books.append(book)
                    Exporter.download_image(book.image_url, book.category, book.title)

            if books:
                Exporter.export_to_csv(books, books[0].category)

        print("Scraping terminé avec succès.")


   
