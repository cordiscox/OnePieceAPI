from config import db
from flask import jsonify, abort
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from models.user import User
from webargs import fields
from webargs.flaskparser import use_args
from flasgger import swag_from



user_args = {
    'username': fields.Str(required=True),
    'password': fields.Str(required=True)
}

class LoginResource(Resource):
    @use_args(user_args)
    @swag_from('../swagger/user_login.yml')
    def post(self, args):
        username = args['username']
        password = args['password']

        # Verify user credentials in the database
        user = User.query.filter_by(username=username).one_or_none()

        if user and user.password == password:
            access_token = create_access_token(identity=user.id_user)
            return jsonify({'access_token': access_token})
        else:
            abort(404, "Invalid credentials")
            

class RegisterResource(Resource):
    @use_args(user_args)
    @swag_from('../swagger/user_register.yml')
    def post(self, args):
        username = args['username']
        password = args['password']
        print(username)
        print(password)
        # Check if the user already exists
        if User.query.filter_by(username=username).first():
            abort(404, "Username already taken")
        
        # Create a new user
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        # Generate and return an access token
        access_token = create_access_token(identity=user.id_user)
        return jsonify({'message': f'User: {user.username}, created correctly',
                        'access_token': access_token})

