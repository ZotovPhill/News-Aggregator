class Article:
    """
    Represent the Article object. Method __repr__ returns the object
    representation in dictionary.
    """

    def __init__(self, article_name, article_link, article_header, article_text):
        self._name = article_name
        self.link = article_link
        self.header = article_header
        self.text = article_text
