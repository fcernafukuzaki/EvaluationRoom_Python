import datetime
from configs.resources import db, ma
from .candidate_telephone import CandidateTelephone, CandidateTelephoneSchema
from .candidate_form.candidato_direccion import CandidatoDireccion, CandidatoDireccionSchema
from .candidate_psychologicaltest import CandidatePsychologicalTest, CandidatePsychologicalTestSchema

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
    fecharegistro = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    iddocumentoidentidad = db.Column(db.Integer)
    numerodocumentoidentidad = db.Column(db.String())
    idestadocivil = db.Column(db.Integer)
    cantidadhijos = db.Column(db.Integer)
    idsexo = db.Column(db.Integer)

    telephones = db.relationship('CandidateTelephone', lazy="dynamic", 
                primaryjoin='and_(Candidate.idcandidato==CandidateTelephone.idcandidato)')
    
    addresses = db.relationship('CandidatoDireccion', lazy="dynamic", 
                primaryjoin='and_(Candidate.idcandidato==CandidatoDireccion.idcandidato)')
    
    psychologicaltests = db.relationship('CandidatePsychologicalTest', lazy="dynamic", 
                primaryjoin='and_(Candidate.idcandidato==CandidatePsychologicalTest.idcandidato)')

    def __init__(self, idcandidato, nombre, apellidopaterno, apellidomaterno, iddocumentoidentidad, numerodocumentoidentidad, idestadocivil,
                 cantidadhijos, fechanacimiento, correoelectronico, idsexo, selfregistration):
        self.idcandidato = idcandidato
        self.nombre = nombre
        self.apellidopaterno = apellidopaterno
        self.apellidomaterno = apellidomaterno
        self.iddocumentoidentidad = iddocumentoidentidad
        self.numerodocumentoidentidad = numerodocumentoidentidad
        self.idestadocivil = idestadocivil
        self.cantidadhijos = cantidadhijos
        self.fechanacimiento = fechanacimiento
        self.correoelectronico = correoelectronico
        self.idsexo = idsexo
        self.selfregistration = selfregistration

class CandidateSchema(ma.Schema):
    class Meta:
        fields = ('idcandidato', 'nombre', 'apellidopaterno', 'apellidomaterno', 'fechanacimiento', 'correoelectronico', 'selfregistration',
            'telephones', 'psychologicaltests', 'fecharegistro')
    
    telephones = ma.Nested(CandidateTelephoneSchema, many=True)
    psychologicaltests = ma.Nested(CandidatePsychologicalTestSchema, many=True)

class CandidateDataSchema(ma.Schema):
    class Meta:
        fields = ('idcandidato', 'nombre', 'apellidopaterno', 'apellidomaterno', 'fechanacimiento', 'correoelectronico', 'selfregistration',
            'iddocumentoidentidad','numerodocumentoidentidad','idestadocivil','cantidadhijos','idsexo',
            'telephones', 'addresses', 'psychologicaltests', 'fecharegistro')
    
    telephones = ma.Nested(CandidateTelephoneSchema, many=True)
    addresses = ma.Nested(CandidatoDireccionSchema, many=True)
    psychologicaltests = ma.Nested(CandidatePsychologicalTestSchema, many=True)

class CandidateEmailValidateSchema(ma.Schema):
    class Meta:
        fields = ('idcandidato', 'selfregistration')
