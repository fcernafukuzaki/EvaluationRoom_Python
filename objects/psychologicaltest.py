from configs.flask_config import db, ma
from objects.menu.testpsicologico_instrucciones import TestPsicologicoInstrucciones, TestPsicologicoInstruccionesSchema

class PsychologicalTest(db.Model):
    __table_args__ = {"schema": "evaluationroom"}
    __tablename__ = 'testpsicologico'
    
    idtestpsicologico = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    cantidadpreguntas = db.Column(db.Integer)

    instrucciones = db.relationship('TestPsicologicoInstrucciones', lazy="dynamic", 
                primaryjoin='and_(PsychologicalTest.idtestpsicologico==TestPsicologicoInstrucciones.idtestpsicologico)',
                order_by="and_(TestPsicologicoInstrucciones.idtestpsicologico,TestPsicologicoInstrucciones.idparte)")
    
    def __init__(self, id_psychologicaltest, name=None, quantity_questions=0):
        self.idtestpsicologico = id_psychologicaltest
        self.nombre = name
        self.cantidadpreguntas = quantity_questions
    
class PsychologicalTestSchema(ma.Schema):
    class Meta:
        fields = ('idtestpsicologico', 'nombre', 'cantidadpreguntas')

class PsychologicalTestInfoSchema(ma.Schema):
    class Meta:
        fields = ('idtestpsicologico', 'nombre', 'cantidadpreguntas', 'instrucciones')
    
    instrucciones = ma.Nested(TestPsicologicoInstruccionesSchema, many=True)