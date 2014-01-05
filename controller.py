import os
from flask import Flask,render_template
import random


app = Flask(__name__)

@app.route('/')
def hello():

    return render_template('home.html')





