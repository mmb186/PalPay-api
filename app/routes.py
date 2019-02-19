from flask import jsonify, request

from app import app, bcrypt
from app.auth.utilities import AuthToken, ResponseCreator
from app.auth.utilities import login_required_jwt
from app.models.BlackListedToken import BlackListedToken
from app.models.Tabs.Tab import Tab, TabStatus
from app.models.Tabs.UserTabStatus import TabUserStatus, UserTabStatus
from app.models.User import User
from app.utilities.utilities_data_view_generator import create_tab_view_dictionary, has_all_users_approved
from app.utilities.validators import is_valid_user_info, is_valid_email


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
            password=User.generate_hash(data['password']),
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username']
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
def protected_resource(current_user):
    return jsonify({'status': 'Protected'})


@app.route('/api/get_all_users/', methods=['GET'])
@login_required_jwt
def get_all_users(current_user):
    users = User.get_all()
    users_response = []
    for user in users:
        users_response.append({
            'username': user.username,
            'fullname': user.first_name + ' ' + user.last_name,
            'email': user.email
        })
    return jsonify({'users': users_response})


@app.route('/api/add_trusted_contact/', methods=['POST'])
@login_required_jwt
def add_trusted_contact(current_user):
    contact = User.get_by_username(request.get_json()['username'])
    if contact is not None:
        current_user.add_contact(contact)
        current_user.save()
        return ResponseCreator.response(
            'success',
            f'Added {contact.username} to trusted contacts',
            200
        )
    return ResponseCreator.response(
        'error',
        f'user: {contact.username} was not found',
        201
    )

# --------------------------------------------------------------------------------
# Tabs
# --------------------------------------------------------------------------------


@app.route('/api/create_new_tab/', methods=['POST'])
@login_required_jwt
def create_new_tab(current_user):
    tab_data = request.get_json()
    other_user = User.get_by_username(tab_data['otheruser'])
    if not other_user.id == current_user.id:
        new_tab = Tab(name=tab_data['name'], created_by_id=current_user.id)
        new_tab.save()

        current_user_tab_status = TabUserStatus(
            tab_id=new_tab.id,
            user_id=current_user.id,
            status=UserTabStatus.APPROVED,
        )
        other_user_tab_status = TabUserStatus(
            tab_id=new_tab.id, user_id=other_user.id
        )
        current_user_tab_status.save()
        other_user_tab_status.save()
        tab_view_data = create_tab_view_dictionary(new_tab, current_user_tab_status)
        return jsonify({'status': 'ok', 'created_tab': tab_view_data})
    else:
        return jsonify({'error': 'Currently, you cannot create a tab with yourself'})


@app.route('/api/set_user_tab_status/', methods=['POST'])
@login_required_jwt
def set_user_tab_status(current_user):
    # TODO: handle decline --> delete/archive Tab

    tab_user_status = TabUserStatus.get_by_tab_id_and_user_id(
        tab_id=request.get_json()['tab_id'],
        user_id=current_user.id,
    )
    if tab_user_status is not None:
        updated_status = request.get_json()['tab_status']
        tab_user_status.update_status(updated_status)
        tab = Tab.get_by_id(tab_user_status.tab_id)
        all_users_approved = has_all_users_approved(tab_user_status)
        if all_users_approved:
            tab.update_tab_status(TabStatus.ACTIVE)
        return jsonify({
            'status': 'ok',
            'updated_tab': create_tab_view_dictionary(tab, tab_user_status)
        })
        pass
    else:
        return jsonify({'status': 'Tab with use does not exist, or was deleted'})













