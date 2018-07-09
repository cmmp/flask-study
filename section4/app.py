from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from marshmallow import Schema, fields, ValidationError

from app_security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'cassio-42' # important!
api = Api(app)

jwt = JWT(app, authenticate, identity) # creates /auth endpoint

items = []

class ItemSchema(Schema):
    price = fields.Float(required=True)

item_schema = ItemSchema()

class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return item if item else {'error': 'could not find item'}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'error': 'item with name {} already exists'.format(name)}, 400

        json_data = request.get_json()
        if not json_data:
            return {'error': 'no input data provided!'}, 400
        # validate and deserialize input
        try:
            data = item_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted'}

    def put(self, name):

        json_data = request.get_json()
        if not json_data:
            return {'error': 'no input data provided!'}, 400
        # validate and deserialize input
        try:
            data = item_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):

    def get(self):
        return {'items': items}, 200

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/item')


def main():
    app.run(debug=True, port=5000)

if __name__ == '__main__':
    main()
