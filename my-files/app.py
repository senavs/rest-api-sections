from flask import Flask, jsonify
from flask_restful import Api
# from flask_jwt import JWT
from flask_jwt_extended import JWTManager

from database import InitDatabase, db
# from security import authenticate, identity
from resources.user import User, UserRegister, UserLogin, TokenRefrash
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['SECRET_KEY'] = 'mypass'


# InitDatabase('data.db')

@app.before_first_request
def create_tables():
    db.create_all()


db.init_app(app)

jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['identity'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return {'description': 'The token has expired',
            'error': 'token_expired'}, 401


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401


api = Api(app)
api.add_resource(Store, '/store')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item')
api.add_resource(ItemList, '/items')
api.add_resource(User, '/user')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefrash, '/refresh')

if __name__ == '__main__':
    app.run(debug=True)
