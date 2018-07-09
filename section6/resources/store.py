from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return  {'error': 'could not find store'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'error': 'store already exists'}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"error": "error ocurred while writing to the database"}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'store deleted'}

class StoreList(Resource):

    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
