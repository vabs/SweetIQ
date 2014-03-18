from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
##this is our data model
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL","sqlite:///home/syed/work/siqreviews/reviews.db")
db = SQLAlchemy(app)

class Location(db.Model):
	location_id = db.Column(db.String(100), primary_key=True)
	account_id = db.Column(db.String(100))
	location_name = db.Column(db.String(200))
	address = db.Column(db.String(200))
	tel = db.Column(db.String(200))
	industry = db.Column(db.String(200))


class Listing(db.Model):
	listing_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	location_id = db.Column(db.String, db.ForeignKey('location.location_id'), index=True)
	domain = db.Column(db.String(150))
	name = db.Column(db.String(150))
	link = db.Column(db.String(500))


class Reviews(db.Model):
	review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  	location_id = db.Column(db.String, db.ForeignKey('location.location_id'), index=True)
	rating = db.Column(db.Integer)
	comment = db.Column(db.String(500))
	accuracy = db.Column(db.String(500))
	

