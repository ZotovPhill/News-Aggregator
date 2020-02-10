import ast

from flask import jsonify, render_template, url_for, request, redirect

from scraper import app, db, articles_schema
from scraper.models.database_article import ArticleDB
from scraper.scraperfactory.sitescraper_factory import SiteScraperFactory
from scraper.scraperfactory.multiprocessing_scraper_factory import (
    MultiprocessingScraperFactory,
)


def save_checked_article_to_database():
    """
    Method writes to the database values presented on page with
    marked checkbox.
    """
    # Selected value will be put into a list from checkbox with name
    selected_articles = request.form.getlist("check_article")
    for selected_article in selected_articles:
        # ->dict Evaluating strings containing Python values
        fav_article = ast.literal_eval(selected_article)
        article = ArticleDB(
            _name=fav_article["_name"],
            link=fav_article["link"],
            header=fav_article["header"],
            text=fav_article["text"],
        )
        db.session.add(article)
    db.session.commit()


def delete_checked_article_to_database():
    """
    Method delete from database values presented on page with
    marked checkbox.
    """
    selected_articles = request.form.getlist("check_article")
    for selected_article in selected_articles:
        fav_article = ast.literal_eval(selected_article)
        db.session.query(ArticleDB).filter(
            ArticleDB.header == fav_article["header"]
        ).delete()
    db.session.commit()


@app.route("/news", methods=["GET", "POST"])
def get_news():
    """
    At the GET request /news return all of the following collected news
    articles from various sites and converting to JSON format
    """
    if request.method == "POST":
        save_checked_article_to_database()
        return redirect(url_for("read_later", type="else"))

    site_scraper = SiteScraperFactory()
    scraping_result = {
        "DEV.BY": site_scraper.scrap_all_articles("dev.by"),
        "THE VERGE": site_scraper.scrap_all_articles("theverge"),
        "TECH ONLINER": site_scraper.scrap_all_articles("onliner"),
    }
    """
    To return different response objects in one route for different
    cases: render_template return unicode that transform to valid Response and
    jsonify return already Response object, so we can use both in same route
    """
    if request.args["type"] == "json":
        return jsonify(scraping_result)
    else:
        return render_template(
            "news.html", news_feed=scraping_result, checkbox_label="Read later"
        )


@app.route("/news/<site>", methods=["GET", "POST"])
def get_single_news(site):
    """
    At the GET request /news/<site>, current news is exclusively provided on
    <site>
    """
    # Send post request after submitting and save checked articles in database
    if request.method == "POST":
        save_checked_article_to_database()
        return redirect(url_for("read_later", type="else"))

    site_scraper = SiteScraperFactory()
    scraping_result = {site: site_scraper.scrap_all_articles(site)}
    if request.args["type"] == "json":
        return jsonify(scraping_result)
    else:
        return render_template(
            "news.html", news_feed=scraping_result, checkbox_label="Read later"
        )


@app.route("/multinews", methods=["GET", "POST"])
def multinews():
    """
    Function provide a multithread version of Scraper
    """
    if request.method == "POST":
        save_checked_article_to_database()
        return redirect(url_for("read_later", type="else"))

    site_scraper = MultiprocessingScraperFactory()
    scraping_result = {
        "DEV.BY": site_scraper.scrap_all_articles("dev.by"),
        "THE VERGE": site_scraper.scrap_all_articles("theverge"),
        "TECH ONLINER": site_scraper.scrap_all_articles("onliner"),
    }
    if request.args["type"] == "json":
        return jsonify(scraping_result)
    else:
        return render_template(
            "news.html", news_feed=scraping_result, checkbox_label="Read later"
        )


@app.route("/favorite", methods=["GET", "POST"])
def read_later():
    """
    Function retrieve data from a database and serializing it into a standard
    view of a python object
    """
    if request.method == "POST":
        delete_checked_article_to_database()
        return redirect(url_for("read_later", type="else"))

    all_articles = ArticleDB.query.all()
    result = articles_schema.dump(all_articles)
    news_feed = {"Left for Later": result}
    if request.args["type"] == "json":
        return jsonify(news_feed)
    else:
        return render_template(
            "news.html", news_feed=news_feed, checkbox_label="Delete article"
        )


@app.route("/home")
def home():
    """
    Main Page
    """
    return render_template("home.html")
