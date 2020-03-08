from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps
from db_model import *

Init()

app = Flask(__name__)
app.config["SECRET_KEY"] = "thisissecretkey"


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    return response


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwag):
        if not request.headers.has_key("Bearer"):
            return jsonify({'message': 'Token must be in header Bearer'}), 401

        token = request.headers["Bearer"]
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            user = CUser.get_by_id(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(user, *args, **kwag)

    return decorated


@app.route('/say')
@token_required
def index(user):
    return f"Hi {user.username}!"


@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    if ('username' not in data.keys() or 'password' not in data.keys()):
        return jsonify({'message': 'Invalid fields'}), 401

    user = CUser.get_or_none(CUser.username == data['username'])
    if user is not None:
        return jsonify({'message': 'username is not avialable'}), 401

    user = CUser.create(
        username=data['username'],
        password=data['password'],
        is_active=False,
        is_telegramm_auth=False)
    user.save()
    return jsonify({'message': 'successful'}), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if ('username' not in data.keys() or 'password' not in data.keys()):  # Need wrapper
        return jsonify({'message': 'Invalid fields'}), 401

    user = CUser.get(
        (CUser.username == data['username']) &
        (CUser.password == data['password'])
    )

    if (user is None):
        return jsonify({'message': 'Invalid pair login:password'})

    token = jwt.encode(
        {
            'user_id': user.rowid,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365)
        },
        app.config['SECRET_KEY']
    )

    return jsonify({'message': 'Successful', 'token': token.decode('UTF-8')})


app.run(debug=True)
