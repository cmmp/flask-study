from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from marshmallow import Schema, fields, ValidationError

from app_security import authenticate, identity

from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.secret_key = 'cassio-42' # important!
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
api = Api(app)

@app.before_first_request
def create_tables():
    from db import db
    db.create_all()

jwt = JWT(app, authenticate, identity) # creates /auth endpoint

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/item')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/store')


def main():
    from db import db
    db.init_app(app)
    app.run(debug=True, port=5000)

if __name__ == '__main__':
    main()
