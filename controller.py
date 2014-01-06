import os
from flask import Flask,render_template,session,request
import random
import uuid
import json
import requests

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
    #print params 
    #session['id'] = uuid.uuid4().hex
    #session['name'] =  params.get('name')
    #session['address'] =  params.get('address')
    #session['phone'] =  params.get('phone')

    name = params.get('name')
    address = params.get('address')
    phone = params.get('phone')


    print "Find Location"
   
    listing_callback_url =  APP_URL + 'listing_callback'
    review_callback_url =  APP_URL + 'review_callback'
    completed_callback_url =  APP_URL + 'completed_callback'

    print "Listing callback " , listing_callback_url
    print "Review callback " , review_callback_url

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
    app.tokens[token_id] = 0
    return token_id


@app.route('/isComplete/<token_id>')
def is_complete(token_id):
    print "IS complete"
    print app.tokens
    print token_id
    return app.tokens[token_id]


@app.route('/getData/<token_id>')
def get_data(token_id):
    return render_template('listings.html', {'all_listings' : { 'name': "Test", 
                    'listings': []
            }})



@app.route('/listing_callback', methods = ['GET', 'POST'])
def listing_callback():
    print "listing callback"
    print app.tokens
    print request.form
    return "OK"


@app.route('/review_callback', methods = ['GET', 'POST'])
def review_callback():
    print "review callback"
    print app.tokens
    print request.form
    return "OK"

@app.route('/completed_callback', methods = ['GET', 'POST'])
def completed_callback():
    print "completed callback"
    print app.tokens
    print request.form
    return "OK"


