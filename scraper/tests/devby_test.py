import unittest
from scraper.site_scrapers.devbyscraper import DevByScraper


class DevByTest(unittest.TestCase):
    def setUp(self):
        self.scraper = DevByScraper()

    def test_scraping_data(self):
        article = self.scraper.scrap_article(
            "/news/ilon-mask-za-chas-razbogatel-na-usd-2-3-mlrd"
        )

        self.assertEqual(article[0], "dev.by")
        self.assertEqual(
            article[1],
            "https://www.dev.by/news/ilon-mask-za-chas-razbogatel-na-usd-2-3-mlrd",
        )
        clean = self.scraper.clean_data(*article)

        self.assertEqual(
            clean[2], "Илон Маск за час разбогател на $2,3 млрд",
        )

    def test_scraping_of_link(self):
        article = self.scraper.get_links()

        self.assertIn("/news/ilon-mask-za-chas-razbogatel-na-usd-2-3-mlrd", article)


if __name__ == "__main__":
    unittest.main()
