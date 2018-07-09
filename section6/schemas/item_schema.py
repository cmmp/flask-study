from marshmallow import Schema, fields

class ItemSchema(Schema):
    price = fields.Float(required=True)
    store_id = fields.Integer(required=True)
