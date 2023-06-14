from configs.flask_config import db, ma
from .candidate import Candidate
from .candidate_psychologicaltest import CandidatePsychologicalTest
from .candidate_telephone import CandidateTelephone

class CandidateInfo():
    all_candidates_resumen = db.session.query(
                    Candidate.idcandidato, 
                    Candidate.nombre,
                    Candidate.apellidopaterno,
                    Candidate.apellidomaterno,
                    db.func.concat(Candidate.nombre, ' ', Candidate.apellidopaterno, ' ', Candidate.apellidomaterno).label('nombre_completo'),
                    Candidate.fechanacimiento,
                    Candidate.fecharegistro.label('fecha_registro'),
                    Candidate.correoelectronico,
                    # db.session.query(CandidateTelephone.numero
                    #     ).filter(CandidateTelephone.idtelefono==1, 
                    #         CandidateTelephone.idcandidato==Candidate.idcandidato
                    #     ).label('telefono_movil'),
                    # db.session.query(CandidateTelephone.numero
                    #     ).filter(CandidateTelephone.idtelefono==2, 
                    #         CandidateTelephone.idcandidato==Candidate.idcandidato
                    #     ).label('telefono_fijo'),
                    db.func.count(Candidate.idcandidato).label('cant_puestos_laborales'),
                    db.func.count(Candidate.idcandidato).label('cant_examenes_asignados'),
                    db.session.query(db.func.count(CandidatePsychologicalTest.fechaexamen)
                            ).filter(CandidatePsychologicalTest.idcandidato==Candidate.idcandidato,
                                db.or_(
                                    (db.and_(
                                        db.func.extract('year', CandidatePsychologicalTest.fechaexamen) != '1900',
                                        db.func.extract('month', CandidatePsychologicalTest.fechaexamen) != '01',
                                        db.func.extract('day', CandidatePsychologicalTest.fechaexamen) != '01')),
                                    (CandidatePsychologicalTest.fechaexamen!=None)
                                )
                            ).label('tiene_resultado'),
                    Candidate.selfregistration
                ).group_by(Candidate.idcandidato
                ).order_by(Candidate.idcandidato.desc())
            
class CandidateInfoSchema(ma.Schema):
    class Meta:
        fields = ('cant_puestos_laborales', 'cant_examenes_asignados', 'tiene_resultado',
                'idcandidato', 'nombre', 'apellidopaterno', 'apellidomaterno', 'nombre_completo', 'fechanacimiento', 'correoelectronico', 'selfregistration',
                'telefono_fijo', 'telefono_movil', 'fecha_registro')
