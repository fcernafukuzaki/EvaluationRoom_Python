from ..flask_config import db, ma

class JobPositionCandidate(db.Model):
    __table_args__ = {"schema": "evaluationroom"}
    __tablename__ = 'puestolaboralcandidato'
    
    idcliente = db.Column(db.Integer, db.ForeignKey('evaluationroom.cliente.idcliente'), primary_key=True)
    idpuestolaboral = db.Column(db.Integer, db.ForeignKey('evaluationroom.puestolaboral.idpuestolaboral'), primary_key=True)
    idcandidato = db.Column(db.Integer, db.ForeignKey('evaluationroom.candidato.idcandidato'), primary_key=True)
    
    def __init__(self, id_client, id_jobposition, id_candidate):
        self.idcliente = id_client
        self.idpuestolaboral = id_jobposition
        self.idcandidato = id_candidate

class JobPositionCandidateSchema(ma.Schema):
    class Meta:
        fields = ('idcliente', 'idpuestolaboral', 'idcandidato')
