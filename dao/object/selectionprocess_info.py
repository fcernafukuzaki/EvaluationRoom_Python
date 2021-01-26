from dao.flask_config import db, ma
from object.selectionprocess import SelectionProcess
from object.client import Client, ClientSchema
from object.jobposition import JobPosition
from object.selectionprocess_candidate import SelectionProcessCandidate, SelectionProcessCandidateSchema, SelectionProcessCandidateInfoSchema
from object.candidate_info import CandidateInfo, CandidateInfoSchema
from object.candidate import Candidate
from object.candidate_psychologicaltest import CandidatePsychologicalTest
from object.candidate_telephone import CandidateTelephone
from object.psychologicaltest import PsychologicalTest
from datetime import datetime, timedelta


class SelectionProcessInfo():
    
    resumen = db.session.query(
            db.func.count(SelectionProcess.process_active).label('cant_procesos_activos'),'1'
        ).filter(SelectionProcess.process_active==True
        ).group_by(SelectionProcess.process_active)
                    
    def selectionprocess_info(processStatus='True'):
        filtroSelectionProcess = SelectionProcess.process_active==True
        if processStatus == 'False':
            filtroSelectionProcess = SelectionProcess.process_active==False
        elif processStatus == 'All':
            filtroSelectionProcess = db.or_(SelectionProcess.process_active==True, SelectionProcess.process_active==False)

        all_processselection_resumen = db.session.query(
                        SelectionProcess.idclient,
                        Client.nombre.label('client_name'),
                        SelectionProcess.date_process_begin,
                        SelectionProcess.date_process_end,
                        SelectionProcess.idjobposition,
                        JobPosition.nombre.label('jobposition_name'),
                        SelectionProcess.process_active,
                        SelectionProcess.user_register,
                        Candidate.idcandidato, 
                        Candidate.nombre,
                        Candidate.apellidopaterno,
                        Candidate.apellidomaterno,
                        Candidate.fechanacimiento,
                        Candidate.correoelectronico,
                        db.session.query(CandidateTelephone.numero
                            ).filter(CandidateTelephone.idtelefono==1, 
                                CandidateTelephone.idcandidato==Candidate.idcandidato
                            ).label('telefono_movil'),
                        db.session.query(CandidateTelephone.numero
                            ).filter(CandidateTelephone.idtelefono==2, 
                                CandidateTelephone.idcandidato==Candidate.idcandidato
                            ).label('telefono_fijo'),
                        db.func.count(Candidate.idcandidato).label('cant_puestos_laborales'),
                        db.func.count(Candidate.idcandidato).label('cant_examenes_asignados'),
                        db.session.query(db.func.count(CandidatePsychologicalTest.fechaexamen)
                            ).filter(CandidatePsychologicalTest.idcandidato==Candidate.idcandidato,
                                db.func.extract('year', CandidatePsychologicalTest.fechaexamen) != '1900',
                                db.func.extract('month', CandidatePsychologicalTest.fechaexamen) != '01',
                                db.func.extract('day', CandidatePsychologicalTest.fechaexamen) != '01'
                            ).label('tiene_resultado'),
                        Candidate.selfregistration
                    ).filter(filtroSelectionProcess
                    ).outerjoin(Client, 
                        SelectionProcess.idclient==Client.idcliente
                    ).outerjoin(JobPosition, 
                        SelectionProcess.idjobposition==JobPosition.idpuestolaboral
                    ).outerjoin(SelectionProcessCandidate, 
                        SelectionProcess.idjobposition==SelectionProcessCandidate.idjobposition
                    ).outerjoin(Candidate, SelectionProcessCandidate.idcandidate==Candidate.idcandidato
                    ).group_by(SelectionProcess.idclient, Client.nombre, Candidate.idcandidato, SelectionProcess.date_process_begin,
                        SelectionProcess.date_process_end,
                        SelectionProcess.idjobposition,
                        JobPosition.nombre
                    ).order_by(SelectionProcess.idclient, SelectionProcess.idjobposition)
        return all_processselection_resumen
    
    def candidates_without_selectionprocess_info():
        subquery = db.session.query(SelectionProcessCandidate.idcandidate)
        all_processselection_resumen = db.session.query(
                        Candidate.idcandidato, 
                        Candidate.nombre,
                        Candidate.apellidopaterno,
                        Candidate.apellidomaterno,
                        Candidate.fechanacimiento,
                        Candidate.correoelectronico,
                        db.session.query(CandidateTelephone.numero
                            ).filter(CandidateTelephone.idtelefono==1, 
                                CandidateTelephone.idcandidato==Candidate.idcandidato
                            ).label('telefono_movil'),
                        db.session.query(CandidateTelephone.numero
                            ).filter(CandidateTelephone.idtelefono==2, 
                                CandidateTelephone.idcandidato==Candidate.idcandidato
                            ).label('telefono_fijo'),
                        db.func.count(Candidate.idcandidato).label('cant_examenes_asignados'),
                        db.session.query(db.func.count(CandidatePsychologicalTest.fechaexamen)
                            ).filter(CandidatePsychologicalTest.idcandidato==Candidate.idcandidato,
                                db.func.extract('year', CandidatePsychologicalTest.fechaexamen) != '1900',
                                db.func.extract('month', CandidatePsychologicalTest.fechaexamen) != '01',
                                db.func.extract('day', CandidatePsychologicalTest.fechaexamen) != '01'
                            ).label('tiene_resultado'),
                        Candidate.selfregistration
                    ).filter(Candidate.idcandidato.notin_(subquery)
                    ).group_by(Candidate.idcandidato
                    ).order_by(Candidate.idcandidato.desc())
        return all_processselection_resumen

    def candidates_psychologicaltest_info(processStatus='True'):
        filtroSelectionProcess = SelectionProcess.process_active==True
        if processStatus == 'False':
            filtroSelectionProcess = SelectionProcess.process_active==False
        elif processStatus == 'All':
            filtroSelectionProcess = db.or_(SelectionProcess.process_active==True, SelectionProcess.process_active==False)

        all_candidates_psychologicaltest_resumen = db.session.query(
                        db.func.concat(SelectionProcess.idclient, '_', SelectionProcess.idjobposition, '_', CandidatePsychologicalTest.idcandidato).label('id'),
                        CandidatePsychologicalTest.idcandidato,
                        SelectionProcess.idjobposition,
                        CandidatePsychologicalTest.idtestpsicologico,
                        CandidatePsychologicalTest.fechaexamen,
                        PsychologicalTest.nombre
                    ).filter(filtroSelectionProcess
                    ).outerjoin(SelectionProcessCandidate, 
                        SelectionProcess.idjobposition==SelectionProcessCandidate.idjobposition
                    ).outerjoin(CandidatePsychologicalTest, 
                        SelectionProcessCandidate.idcandidate==CandidatePsychologicalTest.idcandidato
                    ).outerjoin(PsychologicalTest, 
                        CandidatePsychologicalTest.idtestpsicologico==PsychologicalTest.idtestpsicologico
                    ).order_by(CandidatePsychologicalTest.idcandidato, CandidatePsychologicalTest.idtestpsicologico)
        return all_candidates_psychologicaltest_resumen

    def candidates_psychologicaltest_without_selectionprocess_info():
        subquery = db.session.query(SelectionProcessCandidate.idcandidate)
        all_candidates_psychologicaltest_resumen = db.session.query(
                        CandidatePsychologicalTest.idcandidato.label('id'),
                        CandidatePsychologicalTest.idcandidato,
                        CandidatePsychologicalTest.idtestpsicologico,
                        CandidatePsychologicalTest.fechaexamen,
                        PsychologicalTest.nombre
                    ).filter(CandidatePsychologicalTest.idcandidato.notin_(subquery)
                    ).outerjoin(PsychologicalTest, 
                        CandidatePsychologicalTest.idtestpsicologico==PsychologicalTest.idtestpsicologico
                    ).order_by(CandidatePsychologicalTest.idcandidato, CandidatePsychologicalTest.idtestpsicologico)
        return all_candidates_psychologicaltest_resumen

class SelectionProcessInfoResumenSchema(ma.Schema):
    class Meta:
        fields = ('cant_procesos_activos','resumen')
           
class SelectionProcessInfoSchema(ma.Schema):
    class Meta:
        fields = ('idclient', 'client_name', 'date_process_begin', 'date_process_end', 
                'idjobposition', 'jobposition_name',  
                'process_active', 'user_register',
                'cant_candidatos_asignados',
                'cant_puestos_laborales', 'cant_examenes_asignados', 'tiene_resultado',
                'idcandidato', 'nombre', 'apellidopaterno', 'apellidomaterno', 'fechanacimiento', 'correoelectronico', 'selfregistration',
                'telefono_fijo', 'telefono_movil'
                )

class CandidateWithoutSelectionProcessSchema(ma.Schema):
    class Meta:
        fields = ('cant_examenes_asignados', 'tiene_resultado',
                'idcandidato', 'nombre', 'apellidopaterno', 'apellidomaterno', 'fechanacimiento', 'correoelectronico', 'selfregistration',
                'telefono_fijo', 'telefono_movil')

class CandidatePsychologicalTestInfoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'idcandidato', 'idtestpsicologico', 'fechaexamen', 'nombre')

class CandidatePsychologicalTestWithoutSelectionProcessInfoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'idcandidato', 'idtestpsicologico', 'fechaexamen', 'nombre')