class Category:
    """Model class representing a category"""
    
    def __init__(self, name=None, url=None):
        """Initialize a category with optional id and name"""
        self.name = name
        self.url = url
    
    def __str__(self):
        """String representation of the category"""
        return f"Category(name={self.name}, url={self.url})"
