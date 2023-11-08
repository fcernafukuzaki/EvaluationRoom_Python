from configs.resources import db, ma

class JobPosition(db.Model):
    __table_args__ = {"schema": "evaluationroom"}
    __tablename__ = 'puestolaboral'
    
    idcliente = db.Column(db.Integer, db.ForeignKey('evaluationroom.cliente.idcliente'), primary_key=True)
    idpuestolaboral = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String())
    
    def __init__(self, id_client, id_jobposition, name=None):
        self.idcliente = id_client
        self.idpuestolaboral = id_jobposition
        self.nombre = name

class JobPositionSchema(ma.Schema):
    class Meta:
        fields = ('idcliente', 'idpuestolaboral', 'nombre')
