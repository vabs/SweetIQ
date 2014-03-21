import os
from flask import Flask,render_template,session,request, jsonify
import random
import uuid
import json
import requests
from model import db,Listing,Reviews,Location


APP_URL = os.environ.get('URL', 'http://evening-escarpment-1123.herokuapp.com/')
app = Flask(__name__)
app.debug = True
setattr(app,'tokens', {})


@app.route('/')
def hello():
    return render_template('home.html')


@app.route('/find', methods = ['GET', 'POST'])
def find_location():
	params =  request.form
	account = params.get('accountid')
	name = params.get('name')
	address = params.get('address')
	phone = params.get('phone')
	industry = params.get('industry')
	
	print "Find Location"
	
	listing_callback_url =  APP_URL + 'listing_callback'
	review_callback_url =  APP_URL + 'review_callback'
	completed_callback_url =  APP_URL + 'completed_callback'

	#print "Listing callback " , listing_callback_url
	#print "Review callback " , review_callback_url

	req_params = { 
		'location': '{"name": "%s", "address": "%s", "phone": "%s"}' % ( name, address, phone ),
		'listing_callback_url' : listing_callback_url,
		'review_callback_url' : review_callback_url,
		'completed_callback_url': completed_callback_url
	}

	siq_url = 'https://app.ait.gmlapi.com:8080/advance-it'
	response = requests.get(siq_url, params = req_params, verify=False)
	siq_response = json.loads(response.text)
	token_id = siq_response.get('token_id')

	#print "TOKEN ID:  ", token_id
	name = unicode(name)
	address = unicode(address)
	industry = unicode(industry)


	location = Location(location_id = token_id, account_id = account, location_name = name, address = address, tel = phone, industry = industry)

	db.session.add(location)
	try:
		db.session.commit()
	except:
		db.session.rollback()
	finally:
		db.session.close()
	## we use the token id for knowing that the request is the one that we had, either 0 or 1
	app.tokens[token_id] = 0
	return token_id


@app.route('/isComplete/<token_id>')
def is_complete(token_id):
	##for logging
	print "IS complete"
	#print app.tokens
	#print token_id

	if token_id not in app.tokens:
		return "-1"
	app.tokens[token_id] = 1
	return str(app.tokens[token_id])


@app.route('/getData/<token_id>')
def get_data(token_id):     
	location_name = Location.query.get(token_id).location_name
	address = Location.query.get(token_id).address
	telephone = Location.query.get(token_id).tel

	listings = Listing.query.filter(Listing.location_id==token_id).all()
	reviews = Reviews.query.filter(Listing.location_id==token_id).all()

	tot_rating = 0;
	for rev in reviews:
		tot_rating += rev.rating

	rating =  float(tot_rating)/len(reviews)
	rating = "{0:.2f}".format(rating)
	print "Rating " , rating

	return render_template('listings.html', all_listing={ 'name': location_name, 
		'listings':listings, 'rating': rating, 'address':address, 'tel':telephone})


@app.route('/error')
def error():
	render_template('error.html')


@app.route('/listing_callback', methods = ['GET', 'POST'])
def listing_callback():
	print "listing callback"

	listing_resp = json.loads(request.form.get('listing'))
	if listing_resp:
		name = listing_resp.get('name')
		domain = listing_resp.get('domain')
		link = listing_resp.get('link')
		accuracy = listing_resp.get('accuracy')
		
		location_id = request.form.get('token_id')
		listing = Listing(location_id = location_id, name=name, domain=domain, link=link, accuracy=accuracy)

		db.session.add(listing)
		db.session.commit()

	return "OK"


@app.route('/review_callback', methods = ['GET', 'POST'])
def review_callback():
	print "review callback"
	location_id = request.form.get('token_id')
	review_resp = json.loads(request.form.get('review'))
	if review_resp:
		review_id = review_resp.get('review_id')
		rating = review_resp.get('rating')
		comment = review_resp.get('excerpt')
		
		review = Reviews(rating = rating, location_id = location_id, comment = comment)

		db.session.add(review)
		try:
			db.session.commit()
		except:
			db.session.rollback()
		finally:
			db.session.close()

	#print app.tokens
	#print request.form
	return "OK"

@app.route('/completed_callback', methods = ['GET', 'POST'])
def completed_callback():
	print "completed callback"
	#print app.tokens
	#print request.form
	token_id = request.form.get('token_id')
	app.tokens[token_id] = 1
	return "OK"


@app.route('/find_account/<account_id>')
def find_account(account_id):
	#print "finding account"
	response = {}

	ls = Location.query.filter(Location.account_id == account_id).all()
	print "From finding location"
	location_id = ''
	for l in ls:
		location_id = l.location_id

	listings = Listing.query.filter(Listing.location_id == location_id).all()
	reviews = Reviews.query.filter(Reviews.location_id == location_id).all()
	
	#print "Listings found: ", listings

	#print "Reviews found: ", reviews

	
	l_data = []
	r_data = []
	temp = {}
	
	for listing in listings:
		if listing.name is None or listing.name is '' or listing.accuracy < '0.31':
			pass
		else:		
			temp['name'] = listing.name
			temp['domain'] = listing.domain
			temp['link'] = listing.link
			temp['accuracy'] = listing.accuracy

		l_data.append(temp)
		temp = {}
	
	for review in reviews:
		
		temp['rating'] = review.rating
		temp['comment'] = review.comment
		

		r_data.append(temp)
		temp = {}
	
	response['listings'] = l_data
	response['reviews'] = r_data

	return jsonify(**response)
	