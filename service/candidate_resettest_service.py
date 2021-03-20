from flask import jsonify
from sqlalchemy.sql import table, column, text
from sqlalchemy import create_engine
from dao.flask_config import db, DATABASE_URI
from dao.object.candidate_psychologicaltest_history import CandidatePsychologicalTestHistory, CandidatePsychologicalTestHistorySchema

class CandidateResetTestService():

    def reset_candidate_test(self, id_user, idcandidate, idpsychologicaltest):
        try:
            count_times_psychologicaltest = db.session.query(
                db.func.count(CandidatePsychologicalTestHistory.intento).label('intento')
            ).filter(CandidatePsychologicalTestHistory.idcandidato == idcandidate, 
                CandidatePsychologicalTestHistory.idtestpsicologico == idpsychologicaltest
            )

            if count_times_psychologicaltest.count() > 0:
                time = count_times_psychologicaltest[0].intento + 1
                data = ({'time': time, 'idcandidate': idcandidate, 'idtestpsicologico': idpsychologicaltest, 'id_user': id_user},)
                
                sql_insert = text('''INSERT INTO evaluationroom.candidatotest_historico 
                    (intento, idtestpsicologico, idcandidato, fechaexamen, resultado, fecharegistro_usuario, idusuario) 
                    SELECT 
                    :time AS intento, 
                    evaluationroom.candidatotest.idtestpsicologico AS evaluationroom_candidatotest_idtestpsicologico, 
                    evaluationroom.candidatotest.idcandidato AS evaluationroom_candidatotest_idcandidato, 
                    evaluationroom.candidatotest.fechaexamen AS evaluationroom_candidatotest_fechaexamen, 
                    evaluationroom.candidatotest.resultado AS evaluationroom_candidatotest_resultado, now() AS fecharegistro_usuario, 
                    :id_user AS idusuario
                    FROM evaluationroom.candidatotest
                    WHERE evaluationroom.candidatotest.idcandidato = :idcandidate
                    AND evaluationroom.candidatotest.idtestpsicologico = :idtestpsicologico
                    ORDER BY evaluationroom.candidatotest.idcandidato, 
                    evaluationroom.candidatotest.idtestpsicologico ''')

                connection = create_engine(DATABASE_URI)
                
                sql_insert_detail = text('''INSERT INTO evaluationroom.candidatotestdetalle_historico 
                    (intento, idtestpsicologico, idpregunta, idparte, idcandidato, respuesta, fecharegistro, origin, host, user_agent, fecharegistro_usuario, idusuario) 
                    SELECT 
                    :time AS intento, 
                    evaluationroom.candidatotestdetalle.idtestpsicologico, 
                    evaluationroom.candidatotestdetalle.idpregunta, 
                    evaluationroom.candidatotestdetalle.idparte, 
                    evaluationroom.candidatotestdetalle.idcandidato, 
                    evaluationroom.candidatotestdetalle.respuesta, 
                    evaluationroom.candidatotestdetalle.fecharegistro,
                    evaluationroom.candidatotestdetalle.origin, 
                    evaluationroom.candidatotestdetalle.host, 
                    evaluationroom.candidatotestdetalle.user_agent, 
                    now() AS fecharegistro_usuario, 
                    :id_user AS idusuario
                    FROM evaluationroom.candidatotestdetalle
                    WHERE evaluationroom.candidatotestdetalle.idcandidato = :idcandidate
                    AND evaluationroom.candidatotestdetalle.idtestpsicologico = :idtestpsicologico
                    ORDER BY evaluationroom.candidatotestdetalle.idcandidato, 
                    evaluationroom.candidatotestdetalle.idtestpsicologico,
                    evaluationroom.candidatotestdetalle.idparte,
                    evaluationroom.candidatotestdetalle.idpregunta ''')
                
                sql_update = text('''UPDATE evaluationroom.candidatotest 
                    SET resultado = '""', 
                    fechaexamen = '1900-01-01 00:00:00+00' 
                    WHERE 
                    evaluationroom.candidatotest.idcandidato = :idcandidate 
                    AND evaluationroom.candidatotest.idtestpsicologico = :idtestpsicologico ''')

                sql_delete = text('''DELETE FROM evaluationroom.candidatotestdetalle
                    WHERE 
                    evaluationroom.candidatotestdetalle.idcandidato = :idcandidate
                    AND evaluationroom.candidatotestdetalle.idtestpsicologico = :idtestpsicologico ''')
                
                for line in data:
                    connection.execute(sql_insert, **line)
                    connection.execute(sql_insert_detail, **line)
                    connection.execute(sql_update, **line)
                    connection.execute(sql_delete, **line)

            return {'message': 'Inserted'}, 200
        except:
            return {'message': 'Error'}, 503
        
