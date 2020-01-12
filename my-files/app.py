from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from database import Database
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

Database('data.db')

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = 'mypass'

api = Api(app)
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug=True)
