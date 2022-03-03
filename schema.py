from operator import mod
from config import ma
from models import User, Role
from marshmallow import fields


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model=User
        load_instance=True

    id = fields.Integer(dump_only=True) # Here dump_only fields to skip while .load
    email = fields.String()
    username = fields.String()
    password = fields.String()

userschema = UserSchema()
userschemas = UserSchema(many=True)


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        include_fk = True
        load_instance = True

    id = fields.Integer(dump_only=True)

roleschema = RoleSchema()
roleschemas = RoleSchema(many=True)