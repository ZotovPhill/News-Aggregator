class Article:
    """
    Represent the Article object. Method __repr__ returns the object
    representation in dictionary.
    """

    def __init__(
        self, article_name, article_link, article_header, article_text
    ):
        self.article_name = article_name
        self.article_link = article_link
        self.article_header = article_header
        self.article_text = article_text

    def __repr__(self):
        return {
            "_name": self.article_name,
            "link": self.article_link,
            "header": self.article_header,
            "text": self.article_text,
        }
