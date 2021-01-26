from flask import jsonify
from dao.flask_config import db
from dao.object.login_user import LoginUser, LoginUserSchema

login_user_schema = LoginUserSchema()

class LoginUserService():

    def validate_user(self, hash):
        if hash:
            return db.session.query(LoginUser
                ).filter(LoginUser.hash==hash, 
                         LoginUser.date_logout==None, 
                         LoginUser.iduser > 0
                ).first()
        else:
            return None
