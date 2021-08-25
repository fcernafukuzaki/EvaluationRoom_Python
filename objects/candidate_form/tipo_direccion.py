from configs.flask_config import db, ma

class TipoDireccion(db.Model):
    __table_args__ = {"schema": "evaluationroom", 'extend_existing': True}
    __tablename__ = 'tipodireccion'
    
    idtipodireccion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    
    def __init__(self, id_tipodireccion, name=None):
        self.idtipodireccion = id_tipodireccion
        self.nombre = name

class TipoDireccionSchema(ma.Schema):
    class Meta:
        fields = ('idtipodireccion', 'nombre')