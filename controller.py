import os
from flask import Flask
import random


app = Flask(__name__)

@app.route('/')
def hello():


    return 'Form'


@app.route('/findlocation')
def find_location():


