import os
from flask import Flask,render_template,session
import random
import uuid
import json
import requests

APP_URL = os.environ.get('URL', 'localhost')
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('home.html')



@app.route('/find', methods = ['GET', 'POST'])
def find_location():

    params =  request.form
    
    session['id'] = uuid.uuid4().hex
    session['name'] =  params.get('name')
    session['address'] =  params.get('address')
    session['phone'] =  params.get('phone')

   
    listing_callback_url =  APP_URL + 'listing_callback'
    review_callback_url =  APP_URL + 'review_callback'
    completed_callback_url =  APP_URL + 'completed_callback'

    print "Listing callback " , listing_callback_url
    print "Review callback " , review_callback_url

    req_params = { 
        'location': '{"name": "%s", "address": "%s", "phone": "%s"}' % ( name, address, phone )
        'listing_callback_url' : listing_callback_url
        'review_callback_url' : review_callback_url,
        'completed_callback_url': 


    }
    response = request.get(siq_url, params = req_params)
    print "response from siq ", response

    return response.text


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


