import os
import configparser

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.secret_key = "PYTHONTASK"

config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.ini"))
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://%s:%s@%s/%s" % (
    config["mysqlDB"]["user"],
    config["mysqlDB"]["password"],
    config["mysqlDB"]["host"],
    config["mysqlDB"]["database"],
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

from scraper.models.database_article import ArticleSchema

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)

from scraper.routes import route
