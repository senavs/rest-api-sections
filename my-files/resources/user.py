import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, create_access_token,
                                create_refresh_token, jwt_refresh_token_required,
                                get_jwt_identity)

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")

    def post(self):
        data = self.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists.'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'Create user successfully'}


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=int, required=True, help="This field cannot be blank.")

    @jwt_required
    def get(self):
        data = self.parser.parse_args()

        user = UserModel.find_by_id(data['user_id'])
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @jwt_required
    def delete(self):
        data = self.parser.parse_args()

        user = UserModel.find_by_id(data['user_id'])
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")

    def post(self):
        data = self.parser.parse_args()

        user = UserModel.find_by_username(data['username'])
        if user and user.password == data['password']:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {'access_token': access_token, 'refresh_token': refresh_token}

        return {"message": "Invalid Credentials!"}, 401


class TokenRefrash(Resource):

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}