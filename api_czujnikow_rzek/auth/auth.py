from flask import abort, jsonify
from webargs.flaskparser import use_args
from api_czujnikow_rzek.modele import user_schema, User, UserSchema
from api_czujnikow_rzek import db
from api_czujnikow_rzek.auth import auth_bp
from api_czujnikow_rzek.utils import validate_json_content_type, token_required


@auth_bp.route('/register', methods=['POST'])
@validate_json_content_type
@use_args(user_schema, error_status_code=400)
def register(args: dict):
    if User.query.filter(User.username == args['username']).first():
        abort(409, description=f'Użytkownik z podaną nazwą {args["username"]} już istnieje!')
    elif User.query.filter(User.email == args['email']).first():
        abort(409, description=f'Użytkownik z podanym emailem {args["email"]} już istnieje!')

    args['password'] = User.generate_hashed_password(args['password'])
    user = User(**args)
    db.session.add(user)
    db.session.commit()

    token = user.generate_jwt()

    return({
        'success': True,
        'token': token
    })


@auth_bp.route('/login', methods=['POST'])
@validate_json_content_type
@use_args(UserSchema(only=['username', 'password']), error_status_code=400)
def login(args: dict):
    user = User.query.filter(User.username == args['username']).first()

    if not user:
        abort(401, description=f'Błędne dane!')

    if not user.is_password_valid(args['password']):
        abort(401, description=f'Błędne dane!')

    token = user.generate_jwt()

    return({
        'success': True,
        'token': token
    })


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(user_id: str):
    user = User.query.get_or_404(user_id, description=f'User with id {user_id} not found')

    return({
        'success': True,
        'user': user_schema.dump(user)
    })