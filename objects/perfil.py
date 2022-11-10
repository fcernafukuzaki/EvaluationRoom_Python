from configs.flask_config import db, ma

class Perfil(db.Model):
    __table_args__ = {"schema": "evaluationroom", 'extend_existing': True}
    __tablename__ = 'perfil'
    
    idperfil = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    
    def __init__(self, id_perfil=None, nombre=None):
        self.idperfil = id_perfil
        self.nombre = nombre

class PerfilSchema(ma.Schema):
    class Meta:
        fields = ('idperfil','nombre')
