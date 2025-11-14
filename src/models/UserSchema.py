from flask_marshmallow import Marshmallow
from . import app
from src.models.User import User

ma = Marshmallow(app)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)