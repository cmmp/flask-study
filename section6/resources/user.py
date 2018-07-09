import sqlite3
from flask import request
from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError
from models.user import UserModel
from schemas.user_register_schema import UserRegisterSchema

class UserRegister(Resource):
    user_register_schema = UserRegisterSchema()

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'error': 'no input data provided!'}, 400
        try:
            data = UserRegister.user_register_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        if UserModel.find_by_username(data['username']):
            return {'error': 'user {} already exists!'.format(data['username'])}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201
