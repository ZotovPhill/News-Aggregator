import unittest
from scraper.site_scrapers.onlinerscraper import OnlinerScraper


class OnlinerTest(unittest.TestCase):
    def setUp(self):
        self.scraper = OnlinerScraper()

    def test_existence_of_customer(self):
        article = self.scraper.scrap_article("/2020/01/31/wargaming-virus")

        self.assertEqual(article[0], "Tech Onliner")
        self.assertEqual(
            article[1], "https://tech.onliner.by/2020/01/31/wargaming-virus"
        )
        self.assertEqual(
            article[2],
            "Wargaming пожертвует Китаю $10 миллионов на борьбу с коронавирусом",
        )

    def test_scraping_of_link(self):
        article = self.scraper.get_links()

        self.assertIn("/2020/01/31/wargaming-virus", article)


if __name__ == "__main__":
    unittest.main()
