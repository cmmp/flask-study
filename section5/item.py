from flask import request
from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError
from flask_jwt import jwt_required
import sqlite3

class ItemSchema(Schema):
    price = fields.Float(required=True)

item_schema = ItemSchema()

class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return  {'error': 'could not find item'}, 404

    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        conn.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        return None

    def post(self, name):
        if self.find_by_name(name):
            return {'error': 'item already exists'}, 400

        json_data = request.get_json()
        if not json_data:
            return {'error': 'no input data provided!'}, 400
        # validate and deserialize input
        try:
            data = item_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        item = {'name': name, 'price': data['price']}

        try:
            self.insert(item)
        except:
            return {"error": "error ocurred while writing to the database"}, 500

        return item, 201

    def delete(self, name):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        conn.commit()
        conn.close()

        return {'message': 'item deleted'}

    @classmethod
    def insert(cls, item):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        conn.commit()
        conn.close()

    def put(self, name):

        json_data = request.get_json()
        if not json_data:
            return {'error': 'no input data provided!'}, 400
        # validate and deserialize input
        try:
            data = item_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"error": "error ocurred while writing to the database"}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"error": "error ocurred while writing to the database"}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        conn.commit()
        conn.close()


class ItemList(Resource):

    def get(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = [{'name': row[0], 'price': row[1]} for row in result]
        conn.close()

        return {'items': items}, 200
