from ..flask_config import db, ma
from object.candidate_telephone import CandidateTelephone, CandidateTelephoneSchema
from object.candidate_psychologicaltest import CandidatePsychologicalTest, CandidatePsychologicalTestSchema

class Candidate(db.Model):
    __table_args__ = {"schema": "evaluationroom"}
    __tablename__ = 'candidato'
    
    idcandidato = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    apellidopaterno = db.Column(db.String())
    apellidomaterno = db.Column(db.String())
    fechanacimiento = db.Column(db.DateTime)
    correoelectronico = db.Column(db.String())
    selfregistration = db.Column(db.Boolean())

    telephones = db.relationship('CandidateTelephone', lazy="dynamic", 
                primaryjoin='and_(Candidate.idcandidato==CandidateTelephone.idcandidato)')
    
    psychologicaltests = db.relationship('CandidatePsychologicalTest', lazy="dynamic", 
                primaryjoin='and_(Candidate.idcandidato==CandidatePsychologicalTest.idcandidato)')

    def __init__(self, nombre, apellidopaterno, apellidomaterno, fechanacimiento, correoelectronico, selfregistration):
        self.nombre = nombre
        self.apellidopaterno = apellidopaterno
        self.apellidomaterno = apellidomaterno
        self.fechanacimiento = fechanacimiento
        self.correoelectronico = correoelectronico
        self.selfregistration = selfregistration

class CandidateSchema(ma.Schema):
    class Meta:
        fields = ('idcandidato', 'nombre', 'apellidopaterno', 'apellidomaterno', 'fechanacimiento', 'correoelectronico', 'selfregistration',
            'telephones', 'psychologicaltests')
    
    telephones = ma.Nested(CandidateTelephoneSchema, many=True)
    psychologicaltests = ma.Nested(CandidatePsychologicalTestSchema, many=True)
