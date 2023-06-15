from configs.resources import db, ma

class Provincia(db.Model):
    __table_args__ = {"schema": "evaluationroom", 'extend_existing': True}
    __tablename__ = 'provincia'
    
    idpais = db.Column(db.Integer, primary_key=True)
    iddepartamento = db.Column(db.Integer, primary_key=True)
    idprovincia = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    
    def __init__(self, id_country, id_departamento, id_provincia, name=None):
        self.idpais = id_country
        self.iddepartamento = id_departamento
        self.idprovincia = id_provincia
        self.nombre = name

class ProvinciaSchema(ma.Schema):
    class Meta:
        fields = ('idpais', 'iddepartamento', 'idprovincia', 'nombre')