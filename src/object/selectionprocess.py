from ..dao.flask_config import db, ma

class SelectionProcess(db.Model):

    __table_args__ = {"schema": "evaluationroom"}
    __tablename__ = 'selectionprocess'

    idclient = db.Column(db.Integer, primary_key=True)
    idjobposition = db.Column(db.Integer, primary_key=True)
    date_process_begin = db.Column(db.DateTime)
    date_process_end = db.Column(db.DateTime)
    user_register = db.Column(db.String())
    process_active = db.Column(db.Boolean)
    
    def __init__(self, idclient=0, idjobposition=0, date_process_begin=None, date_process_end=None, 
                 user_register=None, process_active=True):
        self.idclient = idclient
        self.idjobposition = idjobposition
        self.date_process_begin = date_process_begin
        self.date_process_end = date_process_end
        self.user_register = user_register
        self.process_active = process_active

class SelectionProcessSchema(ma.Schema):
    class Meta:
        fields = ('idclient', 'idjobposition', 'date_process_begin', 'date_process_end', 
                    'user_register', 'process_active')