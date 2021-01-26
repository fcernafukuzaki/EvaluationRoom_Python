from ..flask_config import db, ma

class Telephone(db.Model):
    __table_args__ = {"schema": "evaluationroom"}
    __tablename__ = 'telefono'
    
    idtelefono = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String())
    
    def __init__(self, id_telephone, type_name=None):
        self.idtelefono = id_telephone
        self.tipo = type_name

class TelephoneSchema(ma.Schema):
    class Meta:
        fields = ('idtelefono', 'tipo')
