import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank!')
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='This field cannot be left blank!')

    price_parser = reqparse.RequestParser()
    price_parser.add_argument('price',
                              type=float,
                              required=True,
                              help='This field cannot be left blank!')

    name_parser = reqparse.RequestParser()
    name_parser.add_argument('name',
                             type=str,
                             required=True,
                             help='This field cannot be left blank!')

    @jwt_required()
    def get(self):
        data = self.name_parser.parse_args()

        item = self.find_by_name(data['name'])

        if item:
            return item
        return {'message': 'Item not found'}, 404

    def post(self):
        data = self.parser.parse_args()

        if self.find_by_name(data['name']):
            return {'message': 'Item already exists'}, 404

        item = {'name': data['name'], 'price': data['price']}

        try:
            Item.insert(item)
        except Exception as err:
            print(err)
            return {"message": "An error occurred inserting the item."}

        return item

    def delete(self):
        data = self.name_parser.parse_args()

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (data['name'],))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    def put(self):
        pass

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        result = cursor.execute('SELECT * FROM items WHERE name=?', (name,))
        result = result.fetchone()

        if result:
            return {'item': result[1], 'price': result[2]}

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(NULL, ?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    pass
