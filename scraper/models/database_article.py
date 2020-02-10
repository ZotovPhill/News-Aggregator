from scraper import db
from scraper import ma


class ArticleDB(db.Model):
    __tablename__ = "article"

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(20), nullable=False)
    link = db.Column(db.String(40), nullable=False)
    header = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(3000), nullable=False)


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ("_name", "link", "header", "text")
