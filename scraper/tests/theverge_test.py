import unittest
from scraper.site_scrapers.thevergescraper import TheVergeScraper


class TheVergeTest(unittest.TestCase):
    def setUp(self):
        self.scraper = TheVergeScraper()

    def test_existence_of_customer(self):
        article = self.scraper.scrap_article(
            "https://www.theverge.com/2020/1/31/21117180/fbi-bezos-hack-amazon-saudi-arabia-nso"
        )

        self.assertEqual(article[0], "The Verge")
        self.assertEqual(
            article[1],
            "https://www.theverge.com/2020/1/31/21117180/fbi-bezos-hack-amazon-saudi-arabia-nso",
        )
        clean = self.scraper.clean_header(article[2])

        self.assertEqual(
            clean,
            "The FBI is investigating the Bezos hack. The agency is looking into Israeli technology firm NSO and whether its software was involved",
        )

    def test_scraping_of_link(self):
        article = self.scraper.get_links()

        # Paste link located on the first page to search in list of links
        self.assertIn(
            "https://www.theverge.com/2020/2/7/21128307/coronavirus-outbreak-tech-industry-production-supply-chain-delay-impact",
            article,
        )


if __name__ == "__main__":
    unittest.main()
