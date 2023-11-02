from app import db
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from models.user import User

class LoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username is required')
    parser.add_argument('password', type=str, required=True, help='Password is required')

    def post(self):
        data = self.parser.parse_args()
        username = data['username']
        password = data['password']

        # Verify user credentials in the database
        user = User.query.filter_by(username=username).one_or_none()

        if user and user.password == password:
            access_token = create_access_token(identity=user.id_user)
            return jsonify({'access_token': access_token})
        else:
            return jsonify({'message': 'Invalid credentials'})
