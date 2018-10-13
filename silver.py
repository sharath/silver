from flask import Flask
from flask import jsonify, request
from flask_pymongo import PyMongo
from flask.ext.bcrypt import Bcrypt
from responses import *
import random, string

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/silver"
db = PyMongo(app).db.silver
bcrypt = Bcrypt(app)


@app.route('/register', methods=['POST'])
def register():
    data = request.form
    user = {'first_name': data['first_name'], 'last_name': data['last_name'], 'username': data['username'],
            'password': data['password'], 'email_address': data['email_address']}

    if db.users.find({'username': user['password']}).count() != 0:
        return REGISTER_ERROR('USER_TAKEN')

    if len(user['password']) < 6:
        return REGISTER_ERROR('SHORT_PASSWORD')

    verification = user['email_address'].split('@')
    if len(verification) < 2:
        return REGISTER_ERROR('INVALID_EMAIL')
    if len(verification[-1].split('.')) < 2:
        return REGISTER_ERROR('INVALID_EMAIL')

    if db.users.find({'email_address': user['email_address']}).count() != 0:
        return REGISTER_ERROR('EMAIL_USED')

    user['password'] = Bcrypt.generate_password_hash(user['password'], 8)
    user_id = db.users.insert_one(user)
    token_entry = {'id': user_id, 'token': ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}

    db.tokens.update({'id': user_id}, token_entry)
    return REGISTER_SUCCESS(**token_entry)


@app.route('/login', methods=['GET'])
def get():
    data = request.form
    username = data['username']
    password = data['password']

    user = db.users.find({'username': username})

    if bcrypt.check_password_hash(user['password'], password):
        token_entry = {'id': user['_id'],
                       'token': ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}
        db.tokens.update({'id': user['_id']}, token_entry)
        return LOGIN_SUCCESS(**token_entry)


@app.route('/')
def status():
    return ROOT_STATUS('running', 'running')
