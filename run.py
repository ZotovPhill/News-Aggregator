from flask import Flask, jsonify

from scraper.scraperfactory.sitescraper_factory import SiteScraperFactory

"""
News aggregator is a REST API service; upon request, it collects headings
and texts of relevant articles from various news sites and returns them in
JSON format.
"""

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


@app.route("/news")
def get_news():
    """
    At the GET request /news return all of the following collected news
    articles from various sites and converting to JSON format
    """
    site_scraper = SiteScraperFactory()
    scraping_result = {
        "DEV.BY": site_scraper.scrap_all_articles("dev.by"),
        "THE VERGE": site_scraper.scrap_all_articles("theverge"),
        "TECH ONLINER": site_scraper.scrap_all_articles("onliner"),
    }

    return jsonify(scraping_result)


@app.route("/news/<site>")
def get_singe_news(site):
    """
    At the GET request /news/<site>, current news is exclusively provided on
    <site>
    """
    site_scraper = SiteScraperFactory()
    scraping_result = site_scraper.scrap_all_articles(site)
    return jsonify(scraping_result)


@app.route("/")
def hello():
    a = "Hello Friend"
    return a


if __name__ == "__main__":
    app.run(debug=True)
