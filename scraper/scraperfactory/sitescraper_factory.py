from scraper.models.article import Article
from scraper.site_scrapers.sitescraper import SiteScraper
from scraper.site_scrapers.devbyscraper import DevByScraper
from scraper.site_scrapers.thevergescraper import TheVergeScraper
from scraper.site_scrapers.onlinerscraper import OnlinerScraper


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
                    (
                        *article_info,
                        raw_article_header,
                        raw_article_text,
                    ) = scraper.scrap_article(link)
                except Exception:
                    continue
                article_header = scraper.clean_header(raw_article_header)
                article_text = scraper.clean_text(raw_article_text)
                article = Article(*article_info, article_header, article_text)
                news_list.append(article.__repr__())
        except Exception as e:
            return str(e)
        return news_list
