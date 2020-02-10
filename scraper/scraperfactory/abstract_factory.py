from scraper.site_scrapers.sitescraper import SiteScraper
from abc import ABC, abstractmethod


class AbstractScraperFactory(ABC):
    """
    The SiteScraperFactory declares the factory method that return an object of
    a SiteScraper class. It contains the logic for scraping articles, that
    where found on the main page of the site, using Scraper object, returned by
    the factory method.
    """

    @abstractmethod
    def _create_scraper(self, site_name: str) -> SiteScraper:
        pass

    @abstractmethod
    def scrap_all_articles(self, site_name):
        pass
