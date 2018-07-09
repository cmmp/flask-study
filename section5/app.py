from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from marshmallow import Schema, fields, ValidationError

from app_security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'cassio-42' # important!
api = Api(app)

jwt = JWT(app, authenticate, identity) # creates /auth endpoint

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/item')
api.add_resource(UserRegister, '/register')


def main():
    app.run(debug=True, port=5000)

if __name__ == '__main__':
    main()
