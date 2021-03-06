import os
from flask import Flask,render_template,session,request, jsonify
import random
import uuid
import json
import requests
import datetime
import time

from pprint import pprint

from model import db,Listing,Reviews,Location



APP_URL = os.environ.get('URL', 'http://evening-escarpment-1123.herokuapp.com/')
app = Flask(__name__)
app.debug = True
setattr(app,'tokens', {})


@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/leadtoaccount/<account_id>&<lead_id>')
def lead_to_account(account_id,lead_id):
	ls = location.query.filter(location.account_id==lead_id).all()
	
	print "changing the lead id to account id"
	
	account_id = ''
	location_id =''
	
	for l in ls:
		location_id = l.location_id
		account_id_from_db = l.account_id
		db.session.query().from_statement("update location set account_id=:account_id where account_id=:lead_id").params().all()
	

	

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
	
	#req_params = {
	#	'api_key' : '@@@@@@@@@@@@@@@@@@@@@',	
	#	'location': '{"name": "%s", "address": "%s", "phone": "%s"}' % ( name, address, phone ),
	#	'listing_callback_url' : listing_callback_url,
	#	'review_callback_url' : review_callback_url,
	#	'completed_callback_url': completed_callback_url
	#}

	siq_url = 'https://app.ait.gmlapi.com:8080/advance-it'
	response = requests.get(siq_url, params = req_params, verify=False)
	siq_response = json.loads(response.text)
	token_id = siq_response.get('token_id')

	#print "TOKEN ID:  ", token_id
	name = unicode(name)
	address = unicode(address)
	industry = unicode(industry)


	location = Location(location_id = token_id, account_id = account, location_name = name, address = address, tel = phone, industry = industry)
	
	#TO-DO: check for duplication account_id in the location table before adding! Remove data from Listing and Review using location_id as the key!
	
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

	#
	listing_resp = json.loads(request.form.get('listing'))
	if listing_resp:
		name = listing_resp.get('name')
		domain = listing_resp.get('domain')
		link = listing_resp.get('link')
		accuracy = "{0:.2f}".format(listing_resp.get('accuracy'))
		listing_hash = request.form.get('unique_hash')
		location_id = request.form.get('token_id')
		listing = Listing(location_id = location_id, name=name, domain=domain, link=link, accuracy=accuracy,unique_hash=listing_hash)

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
		reviewdate = review_resp.get('date')
		review_hash = request.form.get('unique_hash')
		review = Reviews(rating = rating, location_id = location_id, comment = comment, reviewdate = reviewdate, unique_hash=review_hash)

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
		
	charts = db.session.query("count", "average_rating", "month", "unixdate").from_statement("select count(*), avg(rating) as average_rating, date_trunc('month', reviewdate) as month, extract(epoch from date_trunc('month', reviewdate)) * 1000 as unixdate from reviews where location_id = :location_id group by month order by month").params(location_id=location_id).all()
	#reviews = db.session.query('rating', 'comment','reviewdate').from_statement('select rating ,comment,reviewdate from reviews where rating is not null and location_id = :location_id order by reviewdate').params(location_id=location_id).all()
	listings = Listing.query.filter(Listing.location_id == location_id).all()
	reviews = Reviews.query.filter(Reviews.location_id == location_id).all()
	worst_reviews = db.session.query("wrating", "wcomment", "wdomain", "wdate").from_statement("select r.rating as wrating ,r.comment as wcomment,l.domain as wdomain, r.reviewdate as wdate from reviews as r left join listing as l on l.unique_hash=r.unique_hash where r.location_id = :location_id and r.comment!='' order by r.rating, random() limit 3").params(location_id=location_id).all()
	review_stats_raw_result = db.session.query('total', 'average_rating').from_statement("select count(*) as total, avg(rating) as average_rating from reviews where location_id = :location_id").params(location_id=location_id).all()
	star_rating_distribution_raw_result = db.session.query('floor_rating', 'total').from_statement('select floor(rating) as floor_rating, count(*) as total from reviews where rating is not null and location_id = :location_id group by floor_rating order by floor_rating').params(location_id=location_id).all()
	
	l_data = []
	r_data = []
	chart_data = []
	wreview_data=[]
	review_stats = {}
	star_rating_distribution = {}
	temp = {}
	
	pprint(charts)
	
	
	
	if len(worst_reviews) > 0:
		for worst_review in worst_reviews:
			w = {
				'wrating': int(worst_review[0]),
				'wcomment': str(worst_review[1]),
				'wdomain': str(worst_review[2]),
				'wdate': str(worst_review[3])
			}
			wreview_data.append(w)	
	
	for listing in listings:
		#if listing.name is None or listing.name is ''  :
			#pass
		#else:		
		temp['name'] = listing.name
		temp['domain'] = listing.domain
		temp['link'] = listing.link
		temp['accuracy'] = listing.accuracy
		temp['unique_hash']=listing.unique_hash

		l_data.append(temp)
		temp = {}
		
	for chart in charts:
		c = {
			'count': int(chart[0]),
			'average_rating': float(chart[1]),
			'month': str(chart[2]),
			'unixdate': int(chart[3])
		}
		chart_data.append(c)
		
	for review in reviews:
		
		temp['rating'] = review.rating
		temp['comment'] = review.comment		
		r_date = review.reviewdate
		temp['reviewdate'] = r_date.strftime('%d/%m/%Y')
		temp['unique_hash']=review.unique_hash
		temp['unixdate'] =time.mktime(r_date.timetuple())*10000
		r_data.append(temp)
		temp = {}
	
	for stat in review_stats_raw_result:
		review_stats['total_reviews'] = int(stat[0])
		if stat[1]:
			review_stats['average_rating'] = float(stat[1])
		else:
			review_stats['average_rating'] = 0.0
		
	for rating_group in star_rating_distribution_raw_result:
		star_rating_distribution["group%s" % str(int(rating_group[0]))] = int(rating_group[1])
	
	response['listings'] = l_data
	response['reviews'] = r_data
	response['charts'] = chart_data
	response['worst_reviews'] = wreview_data
	response['review_stats'] = review_stats
	response['star_rating_distribution'] = star_rating_distribution

	return jsonify(**response)
	
