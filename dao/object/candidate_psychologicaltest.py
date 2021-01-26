from dao.flask_config import db, ma
from .psychologicaltest import PsychologicalTest, PsychologicalTestSchema

class CandidatePsychologicalTest(db.Model):
    __table_args__ = {"schema": "evaluationroom"}
    __tablename__ = 'candidatotest'
    
    idcandidato = db.Column(db.Integer, db.ForeignKey('evaluationroom.candidato.idcandidato'), primary_key=True)
    idtestpsicologico = db.Column(db.Integer, db.ForeignKey('evaluationroom.testpsicologico.idtestpsicologico'), primary_key=True)
    fechaexamen = db.Column(db.DateTime)
    
    psychologicaltest = db.relationship('PsychologicalTest', 
                primaryjoin='and_(PsychologicalTest.idtestpsicologico==CandidatePsychologicalTest.idtestpsicologico)')
    
    def __init__(self, id_candidate, id_psychologicaltest, date_end_exam=None):
        self.idcandidato = id_candidate
        self.idtestpsicologico = id_psychologicaltest
        self.fechaexamen = date_end_exam
    
class CandidatePsychologicalTestSchema(ma.Schema):
    class Meta:
        fields = ('idcandidato', 'idtestpsicologico', 'fechaexamen', 'psychologicaltest')

    psychologicaltest = ma.Nested(PsychologicalTestSchema)
