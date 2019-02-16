# from manage import jwt
import datetime
from functools import wraps

import jwt
from flask import make_response, jsonify, request

from app import app
from app.models.User import User
from app.models.BlackListedToken import BlackListedToken


class AuthToken:
    @staticmethod
    def get_token_config(user_id):
        return {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'iat': datetime.datetime.utcnow()
        }

    @staticmethod
    def generate_token(user_id):
        return jwt.encode(
            AuthToken.get_token_config(user_id),
            app.config['SECRETE_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def decode_auth_token(token):
        try:
            payload = jwt.decode(token, app.config['SECRETE_KEY'], algorithms='HS256')
            if BlackListedToken.is_black_listed(token):
                return 'Please Sign in again.'
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return 'Token expired, Please Sign again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please SIgn in Again'


class ResponseCreator:
    @staticmethod
    def response_auth(status, message, token, status_code):
        return make_response(jsonify({
            'status': status,
            'message': message,
            'auth_token': token.decode('utf-8')
        })), status_code

    @staticmethod
    def response(status, message, status_code):
        return make_response(jsonify({
            'status': status,
            'message': message,
        })), status_code


def login_required_jwt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            print("login_required_jwt executed")
            token = request.headers['Authorization'].split(" ")[0]
        if not token or BlackListedToken.is_black_listed(token):
            return make_response(jsonify({
                'status': 'failed',
                'message': 'Provide a valid auth token. Log in again please'
            })), 403
        user_id = AuthToken.decode_auth_token(token)
        current_user = User.get_by_id(user_id)
        return f(current_user, *args, **kwargs)
    return decorated_function
