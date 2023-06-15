from configs.resources import db, ma

class Distrito(db.Model):
    __table_args__ = {"schema": "evaluationroom", 'extend_existing': True}
    __tablename__ = 'distrito'
    
    idpais = db.Column(db.Integer, primary_key=True)
    iddepartamento = db.Column(db.Integer, primary_key=True)
    idprovincia = db.Column(db.Integer, primary_key=True)
    iddistrito = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    
    def __init__(self, id_country, id_departamento, id_provincia, id_distrito, name=None):
        self.idpais = id_country
        self.iddepartamento = id_departamento
        self.idprovincia = id_provincia
        self.iddistrito = id_distrito
        self.nombre = name

class DistritoSchema(ma.Schema):
    class Meta:
        fields = ('idpais', 'iddepartamento', 'idprovincia', 'iddistrito', 'nombre')