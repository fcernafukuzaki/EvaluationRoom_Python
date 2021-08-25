from configs.flask_config import db, ma

class Departamento(db.Model):
    __table_args__ = {"schema": "evaluationroom", 'extend_existing': True}
    __tablename__ = 'departamento'
    
    idpais = db.Column(db.Integer, primary_key=True)
    iddepartamento = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    
    def __init__(self, id_country, id_departamento, name=None):
        self.idpais = id_country
        self.iddepartamento = id_departamento
        self.nombre = name

class DepartamentoSchema(ma.Schema):
    class Meta:
        fields = ('idpais', 'iddepartamento', 'nombre')