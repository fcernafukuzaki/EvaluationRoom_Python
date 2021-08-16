from configs.flask_config import db, ma


class CandidatoDireccion(db.Model):
    __table_args__ = {"schema": "evaluationroom"}
    __tablename__ = 'candidatodireccion'

    idcandidato = db.Column(db.Integer, db.ForeignKey('evaluationroom.candidato.idcandidato'), primary_key=True)
    idtipodireccion = db.Column(db.Integer, primary_key=True)
    idpais = db.Column(db.Integer)
    iddepartamento = db.Column(db.Integer)
    idprovincia = db.Column(db.Integer)
    iddistrito = db.Column(db.Integer)
    direccion = db.Column(db.String())

    def __init__(self, idcandidato, idtipodireccion, idpais, iddepartamento, idprovincia, iddistrito, direccion):
        self.idcandidato = idcandidato
        self.idtipodireccion = idtipodireccion
        self.idpais = idpais
        self.iddepartamento = iddepartamento
        self.idprovincia = idprovincia
        self.iddistrito = iddistrito
        self.direccion = direccion


class CandidatoDireccionSchema(ma.Schema):
    class Meta:
        fields = ('idcandidato', 'idtipodireccion', 'idpais', 'iddepartamento', 'idprovincia', 'iddistrito', 'direccion')