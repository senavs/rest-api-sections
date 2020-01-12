import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank!')
    parser.add_argument('name', type=str, required=True, help='This field cannot be left blank!')

    price_parser = reqparse.RequestParser()
    price_parser.add_argument('price', type=float, required=True, help='This field cannot be left blank!')

    name_parser = reqparse.RequestParser()
    name_parser.add_argument('name', type=str, required=True, help='This field cannot be left blank!')

    @jwt_required()
    def get(self):
        data = self.name_parser.parse_args()

        item = ItemModel.find_by_name(data['name'])

        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()

        if ItemModel.find_by_name(data['name']):
            return {'message': 'Item already exists'}, 404

        item = ItemModel(**data)

        try:
            item.insert()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self):
        data = self.name_parser.parse_args()

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (data['name'],))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(data['name'])
        updated_item = ItemModel(**data)

        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occurred inserting the item."}, 500
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error occurred updating the item."}, 500
        return updated_item.json()


class ItemList(Resource):
    pass
