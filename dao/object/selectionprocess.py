from dao.flask_config import db, ma
from object.selectionprocess_candidate import SelectionProcessCandidate, SelectionProcessCandidateSchema, SelectionProcessCandidateInfoSchema
from object.client import Client, ClientSchema
from object.jobposition import JobPosition, JobPositionSchema

class SelectionProcess(db.Model):

    __table_args__ = {"schema": "evaluationroom", 'extend_existing': True}
    __tablename__ = 'selectionprocess'

    idclient = db.Column(db.Integer, db.ForeignKey('evaluationroom.cliente.idcliente'), primary_key=True)
    idjobposition = db.Column(db.Integer, db.ForeignKey('evaluationroom.puestolaboral.idpuestolaboral'), primary_key=True)
    date_process_begin = db.Column(db.DateTime)
    date_process_end = db.Column(db.DateTime)
    user_register = db.Column(db.String())
    process_active = db.Column(db.Boolean)
    selectionprocess_candidates = db.relationship('SelectionProcessCandidate', lazy="dynamic", 
                primaryjoin='and_(SelectionProcess.idclient==SelectionProcessCandidate.idclient, '
                'SelectionProcess.idjobposition==SelectionProcessCandidate.idjobposition)')
    
    client = db.relationship('Client', 
                primaryjoin='and_(SelectionProcess.idclient==Client.idcliente)')

    jobposition = db.relationship('JobPosition', 
                primaryjoin='and_(SelectionProcess.idclient==JobPosition.idcliente, '
                'SelectionProcess.idjobposition==JobPosition.idpuestolaboral)')
    
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
                    'user_register', 'process_active', 'client', 'jobposition', 'selectionprocess_candidates')
        
    client = ma.Nested(ClientSchema)
    jobposition = ma.Nested(JobPositionSchema)
    selectionprocess_candidates = ma.Nested(SelectionProcessCandidateSchema, many=True)

class SelectionProcessInfoSchema(ma.Schema):
    class Meta:
        fields = ('idclient', 'idjobposition', 'date_process_begin', 'date_process_end', 
                    'user_register', 'process_active', 'client', 'jobposition', 'selectionprocess_candidates')
        
    client = ma.Nested(ClientSchema)
    jobposition = ma.Nested(JobPositionSchema)
    selectionprocess_candidates = ma.Nested(SelectionProcessCandidateInfoSchema, many=True)
