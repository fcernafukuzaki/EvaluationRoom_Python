from configs.resources import db, ma
from .telephone import TelephoneSchema

class CandidateTelephone(db.Model):
    __table_args__ = {"schema": "evaluationroom"}
    __tablename__ = 'candidatotelefono'
    
    idcandidato = db.Column(db.Integer, db.ForeignKey('evaluationroom.candidato.idcandidato'), primary_key=True)
    idtelefono = db.Column(db.Integer, db.ForeignKey('evaluationroom.telefono.idtelefono'), primary_key=True)
    numero = db.Column(db.String())

    telephone = db.relationship('Telephone', 
                primaryjoin='and_(Candidate.idcandidato==CandidateTelephone.idcandidato, '
                'CandidateTelephone.idtelefono==Telephone.idtelefono)')
    
    def __init__(self, id_candidato, id_telephone, number=None):
        self.idcandidato = id_candidato
        self.idtelefono = id_telephone
        self.numero = number

class CandidateTelephoneSchema(ma.Schema):
    class Meta:
        fields = ('idcandidato', 'idtelefono', 'numero', 'telephone')

    telephone = ma.Nested(TelephoneSchema)