from configs.flask_config import db, ma

class Sexo(db.Model):
    __table_args__ = {"schema": "evaluationroom", 'extend_existing': True}
    __tablename__ = 'sexo'
    
    idsexo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    
    def __init__(self, id_sexo, name=None):
        self.idsexo = id_sexo
        self.nombre = name

class SexoSchema(ma.Schema):
    class Meta:
        fields = ('idsexo', 'nombre')