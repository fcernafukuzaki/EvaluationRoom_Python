from configs.flask_config import db, ma

class LoginUser(db.Model):
    __table_args__ = {"schema": "evaluationroom"}
    __tablename__ = 'login_user'
    
    iduser = db.Column(db.Integer)
    hash = db.Column(db.String(), primary_key=True)
    date_login = db.Column(db.DateTime)
    date_logout = db.Column(db.DateTime)
    email = db.Column(db.String())

    def __init__(self, iduser, hash, date_login, date_logout=None, email=None):
        self.iduser = iduser
        self.hash = hash
        self.date_login = date_login
        self.date_logout = date_logout
        self.email = email

class LoginUserSchema(ma.Schema):
    class Meta:
        fields = ('iduser', 'hash', 'date_login', 'date_logout', 'email')
