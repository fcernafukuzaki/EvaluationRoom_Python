from configs.resources import db, ma

class Country(db.Model):
    __table_args__ = {"schema": "evaluationroom", 'extend_existing': True}
    __tablename__ = 'pais'
    
    idpais = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    
    def __init__(self, id_country, name=None):
        self.idpais = id_country
        self.nombre = name

class CountrySchema(ma.Schema):
    class Meta:
        fields = ('idpais', 'nombre')