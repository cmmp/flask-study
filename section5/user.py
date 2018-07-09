import sqlite3
from flask import request
from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        conn.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        conn.close()
        return user

class UserRegisterSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

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

        if User.find_by_username(data['username']):
            return {'error': 'user {} already exists!'.format(data['username'])}, 400

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        conn.commit()
        conn.close()

        return {"message": "User created successfully."}, 201
