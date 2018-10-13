from flask import Flask
from flask import jsonify, request
from flask_pymongo import PyMongo
import bcrypt
from responses import *
import random, string

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/silver"
db = PyMongo(app).db.silver


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    print(data)
    user = {'first_name': data['first_name'], 'last_name': data['last_name'], 'username': data['username'],
            'password': data['password'], 'email_address': data['email_address']}

    if db.users.find({'username': user['username']}).count() != 0:
        return REGISTER_ERROR_USER()

    if len(user['password']) < 6:
        return REGISTER_ERROR_PASSWORD()

    verification = user['email_address'].split('@')
    if len(verification) < 2:
        return REGISTER_ERROR_EMAIL()
    if len(verification[-1].split('.')) < 2:
        return REGISTER_ERROR_EMAIL()
    if db.users.find({'email_address': user['email_address']}).count() != 0:
        return REGISTER_ERROR_EMAIL()

    # user['password'] = bcrypt.hashpw(user['password'], bcrypt.gensalt())
    # user_id = db.users.insert_one(user)
    user_id = 'abcde'
    token_entry = {'id': user_id, 'token': ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}

    # db.tokens.update({'id': user_id}, token_entry)
    return REGISTER_SUCCESS(**token_entry)


@app.route('/login', methods=['GET'])
def get():
    data = request.form
    username = data['username']
    password = data['password']

    user = db.users.find({'username': username})

    if bcrypt.checkpw(password, user['password']):
        token_entry = {'id': user['_id'],
                       'token': ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}
        db.tokens.update({'id': user['_id']}, token_entry)
        return LOGIN_SUCCESS(**token_entry)
    LOGIN_ERROR()


@app.route('/')
def status():
    return ROOT_STATUS('running', 'running')
