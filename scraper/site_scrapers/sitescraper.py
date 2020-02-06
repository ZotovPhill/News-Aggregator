import re

import requests

from abc import abstractmethod, ABC


class SiteScraper(ABC):
    """
    SiteScraper interface declares the operations that all concrete scrapers
    must implement. Setting up HEADERS for our requests sending to web server
    """

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) "
        "AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml, "
        "application/xml;q=0.9,image/webp,*/*;q=0.8",
    }

    def __init__(self):
        self.session = requests.Session()

    @abstractmethod
    def get_links(self):
        """
        Get link from the article, and making list of all links presented at
        the main page
        """
        pass

    @abstractmethod
    def scrap_article(self):
        """
        Scrap single article. Makes a transition on concrete link to article
        page. Takes raw article header and text.
        """
        pass

    def clean_header(self, raw_article_header):
        """
        Normalize header and delete extraneous characters.
        """
        article_header = raw_article_header.strip(" ")
        return article_header

    def clean_text(self, raw_article_text):
        """
        Normalize text and delete extraneous characters.
        """
        article_text = " ".join(raw_article_text)
        article_text = re.sub("\n+", "", article_text).strip(" ")
        return article_text
