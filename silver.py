from flask import Flask
from flask import jsonify
from flask_pymongo import PyMongo
from models import *

app = Flask(__name__)


@app.route('/')
def status():
    return jsonify(STATUS_RUNNING)
