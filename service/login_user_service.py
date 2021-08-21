from flask import jsonify
from datetime import datetime, timezone
from configs.flask_config import db
from objects.login_user import LoginUser, LoginUserSchema

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

    def add_login_user(self, id_user, hash, email):
        try:
            date_login = datetime.now(timezone.utc)
            new_login_user = LoginUser(id_user, hash, date_login, email=email)
            db.session.add(new_login_user)
            db.session.commit()
            
            message = 'Se registró login en base de datos.'
            return new_login_user, 200, message
        except Exception as e:
            message = f'Hubo un error al registrar login en base de datos {e}'
            return None, 503, message