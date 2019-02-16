import uuid

from app import app, bcrypt
from flask import jsonify, request

from app.auth.helpers import AuthToken, ResponseCreator
from app.models.BlackListedToken import BlackListedToken
from app.models.User import User
from app.utilities.validators import is_valid_user_info, is_valid_email
from app.auth.helpers import  login_required_jwt

@app.route('/')
def index():
    return "Hello World"


@app.route('/<name>')
def hello_name(name):
    return f'Hello {name}'


@app.route('/api/create_user/', methods=['POST'])
def create_user():
    data = request.get_json()
    if not is_valid_user_info(data) or \
            User.get_user_by_email(data['email']) is not None:
        return jsonify({'error': 'Data was not valid to create a User or a user already exists'}), 500
    else:
        new_user = User(
            email=data['email'],
            public_id=uuid.uuid4(),
            password=User.generate_hash(data['password']),
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        new_user.save()
        return ResponseCreator.response_auth(
            'success',
            "Successfully Registered",
            AuthToken.generate_token(new_user.id),
            201)


@app.route('/api/login/', methods=['POST'])
def login():
    data = request.get_json()
    if is_valid_email(data['email']):
        user = User.get_user_by_email(data['email'])
        if user and bcrypt.check_password_hash(user.password, data['password']):
            return ResponseCreator.response_auth(
                'success',
                'Successfully Logged In',
                AuthToken.generate_token(user.id),
                200)
        return ResponseCreator.response(
            'failed', 'User does not exist or password is incorrect', 401)
    return ResponseCreator.response('failed', 'Invalid Email Address')


# Route will invalidate token everywhere
@app.route('/api/logout/', methods=['POST'])
def logout():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[0]
        token = BlackListedToken(auth_token)
        token.blacklist()
        return ResponseCreator.response('success', 'Successfully Logged out', 200)
    return ResponseCreator.response('failed', 'failed to Log out', 401)


@app.route('/api/protected_resource/', methods=['POST', 'GET'])
@login_required_jwt
def protected_resource():
    return jsonify({'status': 'Protected'})
