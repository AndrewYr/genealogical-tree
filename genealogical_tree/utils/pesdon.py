# from marshmallow import fields, post_load, missing
# from marshmallow import Schema as ClearSchema
# from marshmallow.utils import get_value
#
#
# class Schema(ClearSchema):
#     def get_attribute(cls, attr, obj, default):
#         res = get_value(attr, obj, default=default)
#
#         return res if res is not None else missing
#
#
# class PesronShema(Schema):
#     id = fields.Integer()
#     name = fields.String()
#     parent = fields.List(fields.Nested('PesronShema'))
#
#     @post_load
#     def prepare_data(self, data):
#         return data
