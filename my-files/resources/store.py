from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.store import StoreModel


class Store(Resource):
    name_parser = reqparse.RequestParser()
    name_parser.add_argument('name', type=str, required=True, help='This field cannot be left blank!')

    @jwt_required
    def get(self):
        data = self.name_parser.parse_args()

        store = StoreModel.find_by_name(data['name'])
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    @jwt_required
    def post(self):
        data = self.name_parser.parse_args()

        if StoreModel.find_by_name(data['name']):
            return {'message': f'A store with name {data["name"]} already exist'}, 400

        store = StoreModel(data['name'])
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while creating the store.'}, 400

        return store.json(), 201

    @jwt_required
    def delete(self):
        data = self.name_parser.parse_args()

        store = StoreModel.find_by_name(data['name'])
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):

    @jwt_required
    def get(self):
        return {'stores': [store.json() for store in StoreModel.find_all()]}
