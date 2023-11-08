from configs.resources import db, ma

class Client(db.Model):
    __table_args__ = {"schema": "evaluationroom", 'extend_existing': True}
    __tablename__ = 'cliente'
    
    idcliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    
    def __init__(self, id_client, name=None):
        self.idcliente = id_client
        self.nombre = name

class ClientSchema(ma.Schema):
    class Meta:
        fields = ('idcliente', 'nombre')
