class Book :
    def __init__(self,url,upc, title,price_including_taxe,price_excluding_taxe,number_available,product_description,category,review_rating,image_url):
        self.url = url
        self.upc = upc
        self.title = title
        self.price_including_taxe = price_including_taxe
        self.price_excluding_taxe = price_excluding_taxe
        self.number_available = number_available
        self.product_description = product_description
        self.category = category
        self.review_rating = review_rating
        self.image_url = image_url
        
    def to_dict(self):
        """convert object in dictionnaire."""
        return {
            'product_page_url': self.url,
            'universal_product_code (upc)': self.upc,
            'title': self.title,
            'price_including_taxe': self.price_including_taxe,
            'price_excluding_taxe': self.price_excluding_taxe,
            'number_available': self.number_available,
            'product_description': self.product_description,
            'category': self.category,
            'review_rating': self.review_rating,
            'image_url': self.image_url,
        }