import os
from flask import Flask,render_template,session
import random
import uuid
import json


app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('home.html')



@app.route('/find', methods = ['GET', 'POST'])
def find_location():

    print request.form
    
    session['id'] = uuid.uuid4().hex




