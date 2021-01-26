from dao.flask_config import db, ma
from object.candidate import Candidate, CandidateSchema
from object.candidate_info import CandidateInfoSchema

class SelectionProcessCandidate(db.Model):

    __table_args__ = {"schema": "evaluationroom"}
    __tablename__ = 'selectionprocess_candidate'

    idclient = db.Column(db.Integer, db.ForeignKey('evaluationroom.selectionprocess.idclient'), primary_key=True)
    idjobposition = db.Column(db.Integer, db.ForeignKey('evaluationroom.selectionprocess.idjobposition'), primary_key=True)
    idcandidate = db.Column(db.Integer, db.ForeignKey('evaluationroom.candidato.idcandidato'), primary_key=True)
    
    date_registered = db.Column(db.DateTime)
    user_register = db.Column(db.String())
    user_registered_byself = db.Column(db.Boolean)
    
    candidate = db.relationship('Candidate', 
                primaryjoin='and_(Candidate.idcandidato==SelectionProcessCandidate.idcandidate)')

    def __init__(self, idclient=0, idjobposition=0, idcandidate=0, date_registered=None, 
                 user_register=None, user_registered_byself=True):
        self.idclient = idclient
        self.idjobposition = idjobposition
        self.idcandidate = idcandidate
        self.date_registered = date_registered
        self.user_register = user_register
        self.user_registered_byself = user_registered_byself

class SelectionProcessCandidateSchema(ma.Schema):
    class Meta:
        fields = ('idclient', 'idjobposition', 'idcandidate', 'date_registered', 
                    'user_register', 'user_registered_byself', 'candidate')

    candidate = ma.Nested(CandidateSchema)

class SelectionProcessCandidateInfoSchema(ma.Schema):
    class Meta:
        fields = ('idclient', 'idjobposition', 'idcandidate', 'date_registered', 
                    'user_register', 'user_registered_byself', 'candidate')

    candidate = ma.Nested(CandidateInfoSchema)