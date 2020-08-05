from dao.flask_config import db, ma

class PsychologicalTest(db.Model):
    __table_args__ = {"schema": "evaluationroom"}
    __tablename__ = 'testpsicologico'
    
    idtestpsicologico = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    cantidadpreguntas = db.Column(db.Integer)

    def __init__(self, id_psychologicaltest, name=None, quantity_questions=0):
        self.idtestpsicologico = id_psychologicaltest
        self.nombre = name
        self.cantidadpreguntas = quantity_questions
    
class PsychologicalTestSchema(ma.Schema):
    class Meta:
        fields = ('idtestpsicologico', 'nombre', 'cantidadpreguntas')
