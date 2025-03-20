import os
import csv
import requests
import re

class Exporter:
    
    def download_image(image_url, category, title):
        """Downloads an image and saves it to a folder."""
        category_folder = os.path.join("export", category.replace(" ", "_"))
        os.makedirs(category_folder, exist_ok=True)
        
        sanitized_title = title.replace(" ", "_")
        sanitized_title = re.sub(r'[<>:"/\\|?*\s]', '_', sanitized_title)
        sanitized_title = sanitized_title[:50]
        image_path = os.path.join(category_folder, f"{sanitized_title}.jpg")

        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(image_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image enregistrée : {image_path}")

   
    def export_to_csv(books, category):
        """Exports the data to a CSV file."""
        category_folder = os.path.join("export", category.replace(" ", "_"))
        os.makedirs(category_folder, exist_ok=True)
        file_path = os.path.join(category_folder, f"{category}.csv")

        fieldnames = books[0].__dict__.keys()
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for book in books:
                writer.writerow(book.__dict__)
        
        print(f"Données enregistrées dans : {file_path}")
