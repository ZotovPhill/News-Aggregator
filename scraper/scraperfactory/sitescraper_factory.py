import sys

sys.path.append(".")

from scraper.models.article import Article
from scraper.site_scrapers.sitescraper import SiteScraper
from scraper.site_scrapers.devbyscraper import DevByScraper
from scraper.site_scrapers.thevergescraper import TheVergeScraper
from scraper.site_scrapers.onlinerscraper import OnlinerScraper
import time


class SiteScraperFactory:
    """
    The SiteScraperFactory declares the factory method that return an object of
    a SiteScraper class. It contains the logic for scraping articles, that
    where found on the main page of the site, using Scraper object, returned by
    the factory method.
    """

    def _create_scraper(self, site_name: str) -> SiteScraper:
        scraper: SiteScraper = None
        """
        Application pick scraper type depending on what type is in address bar.
        """
        if site_name == "dev.by":
            scraper = DevByScraper()
        elif site_name == "theverge":
            scraper = TheVergeScraper()
        elif site_name == "onliner":
            scraper = OnlinerScraper()
        else:
            print("No such scraper! Work in progress...")

        return scraper

    def scrap_all_articles(self, site_name):
        scraper: SiteScraper
        """
        Method takes an argument site_name, based on that concrete scraper is
        gonna work. Method get list of links scraped from main page, following
        the recieved links and scrape information from that page. Grab errors
        from requests exception. Return list of dictionary based articles.
        """
        news_list = []
        try:
            scraper = self._create_scraper(site_name)
            links = scraper.get_links()
            for link in links:
                try:
                    raw_article = scraper.scrap_article(link)
                except Exception:
                    continue
                cleared_article = scraper.clean_article(*raw_article)
                article = Article(*cleared_article)
                news_list.append(article.__dict__)
        except Exception as e:
            return str(e)
        return news_list


if __name__ == "__main__":
    start_time = time.time()
    sitescr = SiteScraperFactory()
    sitescr.scrap_all_articles("dev.by")
    result_time = time.time() - start_time
    print(result_time)
