from dao.flask_config import db, ma
from object.candidate import Candidate
from object.candidate_psychologicaltest import CandidatePsychologicalTest

class CandidateInfo():
    all_candidates_resumen = db.session.query(
                    Candidate.idcandidato, 
                    Candidate.nombre,
                    Candidate.apellidopaterno,
                    Candidate.apellidomaterno,
                    Candidate.fechanacimiento,
                    Candidate.correoelectronico,
                    db.func.count(Candidate.idcandidato).label('cant_puestos_laborales'),
                    db.func.count(Candidate.idcandidato).label('cant_examenes_asignados'),
                    db.func.count(CandidatePsychologicalTest.fechaexamen > '1900-01-01').label('tiene_resultado'),
                    Candidate.selfregistration,
                ).outerjoin(CandidatePsychologicalTest, CandidatePsychologicalTest.idcandidato==Candidate.idcandidato).group_by(Candidate.idcandidato).order_by(Candidate.idcandidato)
        
class CandidateInfoSchema(ma.Schema):
    class Meta:
        fields = ('cant_puestos_laborales', 'cant_examenes_asignados', 'tiene_resultado',
                'idcandidato', 'nombre', 'apellidopaterno', 'apellidomaterno', 'fechanacimiento', 'correoelectronico', 'selfregistration')
