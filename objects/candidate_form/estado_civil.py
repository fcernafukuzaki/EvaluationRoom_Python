from configs.flask_config import db, ma

class EstadoCivil(db.Model):
    __table_args__ = {"schema": "evaluationroom", 'extend_existing': True}
    __tablename__ = 'estadocivil'
    
    idestadocivil = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    
    def __init__(self, id_estadocivil, name=None):
        self.idestadocivil = id_estadocivil
        self.nombre = name

class EstadoCivilSchema(ma.Schema):
    class Meta:
        fields = ('idestadocivil', 'nombre')