from flask import Flask
from flask import jsonify, request
from flask_pymongo import PyMongo
from responses import *

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/silver"
db = PyMongo(app).db.silver


@app.route('/register', methods=['POST'])
def register():
    data = request.form
    first_name = data['first_name']
    last_name = data['last_name']
    username = data['username']
    password = data['password']
    email_address = data['email_address']

    if db.users.find({'username': username}).count() != 0:
        return REGISTER_ERROR('USER_TAKEN')

    if len(password)<6:
        return REGISTER_ERROR('SHORT_PASSWORD')

    verification = email_address.split('@')
    if len(verification) < 2:
        return REGISTER_ERROR('INVALID_EMAIL')
    if len(verification[-1].split('.')) < 2:
        return REGISTER_ERROR('INVALID_EMAIL')

    if db.users.find({'email_address': email_address}).count() != 0:
        return REGISTER_ERROR('EMAIL_USED')

    return REGISTER_SUCCESS('idgoeshere', 'sample_token_here')


@app.route('/')
def status():
    return ROOT_STATUS('running', 'running')
