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
        links = [
            link.attrs["href"]
            for link in soup.findAll(
                "a", attrs={"data-analytics-link": ["article", "feature", "review"]},
            )
            if link.attrs["href"] is not None
        ]
        return set(links)

    def scrap_article(self, page):
        req = self.session.get(page, headers=self.HEADERS)
        soup = BeautifulSoup(req.text, features="html5lib")

        article_name = "The Verge"
        article_link = page
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
        return article_name, article_link, raw_article_header, raw_article_text

    def clean_header(self, raw_article_header):
        raw_article_header.pop(0)
        article_header = ". ".join(raw_article_header).strip(" ")
        return article_header

    def clean_text(self, raw_article_text):
        article_text = " ".join(raw_article_text).strip(" ")
        return article_text
