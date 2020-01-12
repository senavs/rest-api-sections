import sqlite3


class UserModel:

    def __init__(self, _id: int, username: str, password: str):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username: str):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE username=?'
        result = cursor.execute(query, (username,)).fetchone()
        if result:
            return cls(*result)
        return None

    @classmethod
    def find_by_id(cls, _id: str):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE id=?'
        result = cursor.execute(query, (_id,)).fetchone()
        if result:
            return cls(*result)
        return None
