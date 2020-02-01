from flask import Flask, jsonify, request, make_response
from jwt import jwt
from functools import wraps
from db_model import *

Init()

app = Flask(__name__)
app.config["SECRET_KEY"] = "thisissecretkey"
# def token_required(f):
#     @wraps
#     def decorated(*args, **kwag):
#         if not request.headers.has_key("Bearer"):
#             return jsonify({'message' : 'Token is missing!'}) ,
#         token = request.headers["Bearer"]

#         try:
#             user = jwt.decode(token, app.config["SECRET_KEY"])
#         except:
#             return jsonify({'message': 'Token is invalid'}), 401


@app.route('/say')
def index():
    return "<H1>Header</H1>"


@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    if ('username' not in data.keys() or 'password' not in data.keys()):
        return jsonify({'message': 'Invalid fields'}), 401

    user = CUser.get_or_none(CUser.username == data['username'])
    if user is not None:
        return jsonify({'message' : 'username is not avialable'}), 401

    user = CUser.create(
        username=data['username'],
        password=data['password'],
        is_active=False,
        is_telegramm_auth=False)
    user.save()
    return jsonify({'message' : 'successful'}), 200


app.run(debug=True)
