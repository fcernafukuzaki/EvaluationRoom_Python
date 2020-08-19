from flask import jsonify
from dao.flask_config import db
from object.login_user import LoginUser, LoginUserSchema

login_user_schema = LoginUserSchema()

class LoginUserService():

    def validate_user(self, hash):
        if hash:
            login_user = LoginUser.query.get((hash))
            print(login_user)
            return login_user
        else:
            return None
