from dao.flask_config import db, ma

class Candidate(db.Model):
    __table_args__ = {"schema": "evaluationroom"}
    __tablename__ = 'candidato'
    
    idcandidato = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    apellidopaterno = db.Column(db.String())

    def __init__(self, nombre, apellidopaterno):
        self.nombre = nombre
        self.apellidopaterno = apellidopaterno

    def serializable(self):
        return {'nombre': self.nombre}

class CandidateSchema(ma.Schema):
    class Meta:
        fields = ('idcandidato', 'nombre', 'apellidopaterno')
