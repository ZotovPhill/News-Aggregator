import re

from bs4 import BeautifulSoup

from scraper.site_scrapers.sitescraper import SiteScraper


class TheVergeScraper(SiteScraper):
    """
    Class provide implementation of SiteScraper interface for concrete site
    "theverge.com". Make list of links based on relevant tags patterns.
    Method "scrap_article" grab header and text of the article at
    the concrete article page.
    """

    URL = "https://www.theverge.com/"

    def __init__(self):
        super().__init__()

    def get_links(self):
        req = self.session.get(self.URL, headers=self.HEADERS)
        soup = BeautifulSoup(req.text, features="html5lib")
        links = []
        for link in soup.findAll(
            "a", attrs={"data-analytics-link": ["article", "feature"]},
        ):
            if link.attrs["href"] is not None:
                links.append(link.attrs["href"])
        return links

    def scrap_article(self, page):
        req = self.session.get(page, headers=self.HEADERS)
        soup = BeautifulSoup(req.text, features="html5lib")
        raw_article_header = [
            header.get_text()
            for header in soup.find("div", class_="c-entry-hero").find_all(
                ["h1", "p"], recursive=True
            )
        ]
        raw_article_text = [
            text.get_text()
            for text in soup.find("div", class_="c-entry-content").find_all(
                ["p", "h3", "li", "a"], recursive=False
            )
        ]
        article_link = page
        article_name = "The Verge"
        return article_name, article_link, raw_article_header, raw_article_text

    def clean_data(
        self, article_name, article_link, raw_article_header, raw_article_text
    ):
        raw_article_header.pop(0)
        header = ". ".join(raw_article_header)
        text = " ".join(raw_article_text)
        text = re.sub("\n+", "", text)
        text = text.strip("\u200b")
        return article_name, article_link, header, text
