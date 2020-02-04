import re

from scraper.site_scrapers.sitescraper import SiteScraper

from bs4 import BeautifulSoup


class OnlinerScraper(SiteScraper):
    """
    Class provide implementation of SiteScraper interface for concrete site
    "tech.onliner.by". Make list of links based on relevant tags and regex
    patterns. Method "scrap_article" grab header and text of the article at
    the concrete article page.
    """

    URL = "https://tech.onliner.by"

    def __init__(self):
        super().__init__()

    def get_links(self):
        req = self.session.get(self.URL, headers=self.HEADERS)
        soup = BeautifulSoup(req.text, features="html5lib")
        links = [
            link.attrs["href"]
            for link in soup.find_all(
                "a",
                class_=["news-tidings__stub", "news-tiles__stub"],
                href=re.compile("^(/2020/)"),
            )
            if link.attrs["href"] is not None
        ]
        return links

    def scrap_article(self, page):
        req = self.session.get(self.URL + page, headers=self.HEADERS)
        soup = BeautifulSoup(req.text, features="html5lib")
        article_name = "Tech Onliner"
        article_link = self.URL + page
        raw_article_header = soup.h1.get_text()
        raw_article_text = [
            text.get_text()
            for text in soup.find("div", class_="news-text").find_all(
                "p", recursive=False
            )
            if not text.strong
        ]
        return article_name, article_link, raw_article_header, raw_article_text
