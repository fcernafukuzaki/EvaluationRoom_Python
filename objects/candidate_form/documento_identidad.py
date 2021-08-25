from configs.flask_config import db, ma

class DocumentoIdentidad(db.Model):
    __table_args__ = {"schema": "evaluationroom", 'extend_existing': True}
    __tablename__ = 'documentoidentidad'
    
    iddocumentoidentidad = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    
    def __init__(self, id_documentoidentidad, name=None):
        self.iddocumentoidentidad = id_documentoidentidad
        self.nombre = name

class DocumentoIdentidadSchema(ma.Schema):
    class Meta:
        fields = ('iddocumentoidentidad', 'nombre')