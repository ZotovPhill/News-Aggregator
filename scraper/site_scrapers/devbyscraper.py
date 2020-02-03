import re
import unicodedata

from scraper.site_scrapers.sitescraper import SiteScraper

from bs4 import BeautifulSoup


class DevByScraper(SiteScraper):
    """
    Class provide implementation of SiteScraper interface for concrete site
    "dev.by". Make list of links based on relevant tags and regex patterns.
    Method "scrap_article" grab header and text of the article at the concrete
    article page.
    """

    URL = "https://www.dev.by"

    def __init__(self):
        super().__init__()

    def get_links(self, page="/news/"):
        req = self.session.get(self.URL + page, headers=self.HEADERS)
        soup = BeautifulSoup(req.text, features="html5lib")
        links = []
        for link in soup.find_all(
            "a", class_="card__link", href=re.compile("^(/news/)((?!:).)*$")
        ):
            if link.attrs["href"] is not None:
                links.append(link.attrs["href"])
        return links

    def scrap_article(self, page):
        req = self.session.get(self.URL + page, headers=self.HEADERS)
        soup = BeautifulSoup(req.text, features="html5lib")
        raw_article_header = soup.find("h1").get_text()
        raw_article_text = [
            text.get_text()
            for text in soup.find("article").find_all(["p", "h4", "h5"], recursive=True)
        ]
        article_link = self.URL + page
        article_name = "dev.by"
        return article_name, article_link, raw_article_header, raw_article_text

    def clean_data(
        self, article_name, article_link, raw_article_header, raw_article_text
    ):
        # Return the normal form for the Unicode string unistr.
        header = unicodedata.normalize("NFKD", raw_article_header)
        header = header.strip(" ")
        text = " ".join(raw_article_text)
        text = unicodedata.normalize("NFKD", text)
        text = re.sub("\ dev.by проводит новое.*", "", text)
        text = re.sub("\n+", "", text)
        # Delete empty whitespace character
        text = text.strip(" ")
        return article_name, article_link, header, text
