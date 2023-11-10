from config import db
from flask import jsonify
from flask import make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from models.user import User

from webargs import fields
from webargs.flaskparser import use_args, use_kwargs, parser, abort

user_args = {
    'username': fields.Str(required=True),
    'password': fields.Str(required=True)
}

class LoginResource(Resource):
    @use_args(user_args)
    def post(self, args):
        username = args['username']
        password = args['password']

        # Verify user credentials in the database
        user = User.query.filter_by(username=username).one_or_none()

        if user and user.password == password:
            access_token = create_access_token(identity=user.id_user)
            return jsonify({'access_token': access_token})
        else:
            response = {'message': 'Invalid credentials'}
            return make_response(response, 400)

class RegisterResource(Resource):
    @use_args(user_args)
    def post(self, args):
        username = args['username']
        password = args['password']

        # Check if the user already exists
        if User.query.filter_by(username=username).first():
            response = {'message': 'Username already taken'}
            return make_response(response, 400)
        
        # Create a new user
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        # Generate and return an access token
        access_token = create_access_token(identity=user.id_user)
        return jsonify({'message': f'User: {user.username}, created correctly',
                        'access_token': access_token})

