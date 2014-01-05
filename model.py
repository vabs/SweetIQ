from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL","sqlite:///home/syed/work/siqreviews/reviews.db")
db = SQLAlchemy(app)

class Location(db.Model):
    location_id = db.Column(db.String(100), primary_key=True)
    account_id = db.Column(db.String(100))
    location_name = db.Column(db.String(200))
    address = db.Column(db.String(200), unique=True)
    tel = db.Column(db.String(200))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class Listing(db.Model):
    listing_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_id = db.Column(db.String, db.ForeignKey('location.location_id'), index=True)
    domain = db.Column(db.String(150))
    name = db.Column(db.String(150))


    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class Reviews(db.Model):
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    listing_id = db.Column(db.String, db.ForeignKey('listing.listing_id'), index=True)
    location_id = db.Column(db.String, db.ForeignKey('location.location_id'), index=True)
    rating = db.Column(db.Integer)
