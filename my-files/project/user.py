import sqlite3
from typing import Union

from flask_restful import Resource, reqparse


class User:

    def __init__(self, _id: int, username: str, password: str):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username: str) -> Union['User', None]:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE username=?'
        result = cursor.execute(query, (username,)).fetchone()
        if result:
            return cls(*result)
        return None

    @classmethod
    def find_by_id(cls, _id: str) -> Union['User', None]:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE id=?'
        result = cursor.execute(query, (_id,)).fetchone()
        if result:
            return cls(*result)
        return None


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")

    def post(self):
        data = self.parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'A user with that username already exists.'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO users VALUES (NULL, ?, ?)", (data['username'], data['password']))
        connection.commit()
        connection.close()

        return {'message': 'Create user successfully'}