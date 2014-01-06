import os
from flask import Flask,render_template,session,request
import random
import uuid
import json
import requests

APP_URL = os.environ.get('URL', 'localhost')
app = Flask(__name__)
app.debug = True

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
    print "response from siq ", response

    return "Hello" 


@app.route('/listing_callback', methods = ['GET', 'POST'])
def listing_callback():
    print "listing callback"
    print request.form


@app.route('/review_callback', methods = ['GET', 'POST'])
def review_callback():
    print "review callback"
    print request.form

@app.route('/completed_callback', methods = ['GET', 'POST'])
def completed_callback():
    print "completed callback"
    print request.form


