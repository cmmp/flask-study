from flask import request
from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError
from flask_jwt import jwt_required
from schemas.item_schema import ItemSchema
from models.item import ItemModel

item_schema = ItemSchema()

class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return  {'error': 'could not find item'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'error': 'item already exists'}, 400

        json_data = request.get_json()
        if not json_data:
            return {'error': 'no input data provided!'}, 400
        # validate and deserialize input
        try:
            data = item_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"error": "error ocurred while writing to the database"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
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

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return updated_item.json()


class ItemList(Resource):

    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
