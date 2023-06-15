from configs.resources import db, ma
from .psychologicaltest import PsychologicalTest, PsychologicalTestSchema

class CandidatePsychologicalTestHistory(db.Model):
    __table_args__ = {"schema": "evaluationroom"}
    __tablename__ = 'candidatotest_historico'
    
    intento = db.Column(db.Integer, primary_key=True)
    idcandidato = db.Column(db.Integer, db.ForeignKey('evaluationroom.candidato.idcandidato'), primary_key=True)
    idtestpsicologico = db.Column(db.Integer, db.ForeignKey('evaluationroom.testpsicologico.idtestpsicologico'), primary_key=True)
    fechaexamen = db.Column(db.DateTime)
    resultado = db.Column(db.String())
    fecharegistro_usuario = db.Column(db.DateTime)
    idusuario = db.Column(db.Integer)
    
    psychologicaltest = db.relationship('PsychologicalTest', 
                primaryjoin='and_(PsychologicalTest.idtestpsicologico==CandidatePsychologicalTestHistory.idtestpsicologico)')
    
    def __init__(self, time, id_candidate, id_psychologicaltest, date_end_exam=None, result=None, registereddate_user=None, iduser=None):
        self.intento = time
        self.idcandidato = id_candidate
        self.idtestpsicologico = id_psychologicaltest
        self.fechaexamen = date_end_exam
        self.resultado = result
        self.fecharegistro_usuario = registereddate_user
        self.idusuario = iduser
    
class CandidatePsychologicalTestHistorySchema(ma.Schema):
    class Meta:
        fields = ('intento', 'idcandidato', 'idtestpsicologico', 'fechaexamen', 
            'resultado', 'fecharegistro_usuario', 'idusuario', 'psychologicaltest')

    psychologicaltest = ma.Nested(PsychologicalTestSchema)
