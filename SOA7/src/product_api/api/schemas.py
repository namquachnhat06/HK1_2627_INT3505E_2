from marshmallow import Schema, fields, validate

# -- Schemas cho Product --
class ProductIn(Schema):
    sku = fields.Str(required=True, validate=validate.Length(min=3, max=32))
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    price_cents = fields.Int(required=True, validate=validate.Range(min=0))
    qty_in_stock = fields.Int(load_default=0, validate=validate.Range(min=0))

class ProductPatch(Schema):
    name = fields.Str()
    price_cents = fields.Int(validate=validate.Range(min=0))

class ReserveIn(Schema):
    qty = fields.Int(required=True, validate=validate.Range(min=1))

class ProductOut(Schema):
    id = fields.Int(dump_only=True)
    sku = fields.Str()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    price_cents = fields.Int()
    qty_in_stock = fields.Int()
    archived = fields.Bool()

# -- Schemas cho Order --
class OrderItemOut(Schema):
    product = fields.Nested(ProductOut)
    quantity = fields.Int()

class OrderOut(Schema):
    id = fields.Int()
    created_at = fields.DateTime()
    items = fields.List(fields.Nested(OrderItemOut))