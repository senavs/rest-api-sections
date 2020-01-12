from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from database import InitDatabase, db
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

InitDatabase('data.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = 'mypass'

db.init_app(app)

api = Api(app)
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug=True)
