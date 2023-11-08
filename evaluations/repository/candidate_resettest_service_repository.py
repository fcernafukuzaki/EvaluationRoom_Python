from configs.resources import db, text
from configs.logging import logger


class CandidateResetTestRepository():
    
    def count_tries(self, idcandidate:int, idpsychologicaltest:int):
        """
        Descripción:
            Contar la cantidad de intentos en un test psicológico asignado a un candidato/paciente.
        Input:
            - idcandidate: Identificador del candidato.
            - idpsychologicaltest: Identificador del test psicológico.
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result: Cantidad de intentos.
        """
        result = None
        try:
            sql_query = f'''SELECT COUNT(ch.intento) AS intento \
                FROM evaluationroom.candidatotest_historico ch \
                WHERE ch.idcandidato = :idcandidato \
                AND ch.idtestpsicologico = :idtestpsicologico \
            '''
            data = {'idcandidato': idcandidate, 'idtestpsicologico': idpsychologicaltest}
            response_database = db.execute(text(sql_query), data)
            
            times_reseted = response_database.fetchone()[0]
            
            logger.debug("Count tries.", idcandidato=idcandidate, idtestpsicologico=idpsychologicaltest, times_reseted=times_reseted)
            result, flag, message = times_reseted, True, 'Se obtuvo la cantidad de intentos en una prueba en base de datos.'
        except Exception as e:
            logger.error("Error.", idcandidato=idcandidate, idtestpsicologico=idpsychologicaltest, error=e)
            db.rollback()
            flag, message = False, f'Hubo un error al obtener la cantidad de intentos de una prueba en base de datos {e}'
        finally:
            logger.debug("Count tries.", message=message)
            return flag, message, result

    def reset(self, iduser:int, idcandidate:int, idpsychologicaltest:int, times:int):
        """
        Descripción:
            Resetear un test psicológico asignado a un candidato/paciente.
        Input:
            - iduser: Identificador del usuario.
            - idcandidate: Identificador del candidato.
            - idpsychologicaltest: Identificador del test psicológico.
            - times: Cantidad de intentos.
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result: Objeto.
        """
        result = None
        try:
            data = {'times': times, 'idcandidate': idcandidate, 'idtestpsicologico': idpsychologicaltest, 'iduser': iduser}
            
            sql_query = '''INSERT INTO evaluationroom.candidatotest_historico \
                (intento, idtestpsicologico, idcandidato, fechaexamen, resultado, fecharegistro_usuario, idusuario) \
                SELECT \
                :times AS intento, \
                evaluationroom.candidatotest.idtestpsicologico AS evaluationroom_candidatotest_idtestpsicologico, \
                evaluationroom.candidatotest.idcandidato AS evaluationroom_candidatotest_idcandidato, \
                evaluationroom.candidatotest.fechaexamen AS evaluationroom_candidatotest_fechaexamen, \
                evaluationroom.candidatotest.resultado AS evaluationroom_candidatotest_resultado, now() AS fecharegistro_usuario, \
                :iduser AS idusuario \
                FROM evaluationroom.candidatotest \
                WHERE evaluationroom.candidatotest.idcandidato = :idcandidate \
                AND evaluationroom.candidatotest.idtestpsicologico = :idtestpsicologico \
                ORDER BY evaluationroom.candidatotest.idcandidato, \
                evaluationroom.candidatotest.idtestpsicologico \
            '''
                
            sql_insert_detail = '''INSERT INTO evaluationroom.candidatotestdetalle_historico \
                (intento, idtestpsicologico, idpregunta, idparte, idcandidato, respuesta, fecharegistro, origin, host, user_agent, fecharegistro_usuario, idusuario) \
                SELECT :times AS intento, \
                evaluationroom.candidatotestdetalle.idtestpsicologico, \
                evaluationroom.candidatotestdetalle.idpregunta, \
                evaluationroom.candidatotestdetalle.idparte, \
                evaluationroom.candidatotestdetalle.idcandidato, \
                evaluationroom.candidatotestdetalle.respuesta, \
                evaluationroom.candidatotestdetalle.fecharegistro, \
                evaluationroom.candidatotestdetalle.origin, \
                evaluationroom.candidatotestdetalle.host, \
                evaluationroom.candidatotestdetalle.user_agent, \
                now() AS fecharegistro_usuario, \
                :iduser AS idusuario \
                FROM evaluationroom.candidatotestdetalle \
                WHERE evaluationroom.candidatotestdetalle.idcandidato = :idcandidate \
                AND evaluationroom.candidatotestdetalle.idtestpsicologico = :idtestpsicologico \
                ORDER BY evaluationroom.candidatotestdetalle.idcandidato, \
                evaluationroom.candidatotestdetalle.idtestpsicologico, \
                evaluationroom.candidatotestdetalle.idparte, \
                evaluationroom.candidatotestdetalle.idpregunta '''
                
            sql_update = '''UPDATE evaluationroom.candidatotest \
                SET resultado = NULL, \
                fechaexamen = NULL \
                WHERE evaluationroom.candidatotest.idcandidato = :idcandidate \
                AND evaluationroom.candidatotest.idtestpsicologico = :idtestpsicologico '''

            sql_delete = '''DELETE FROM evaluationroom.candidatotestdetalle \
                WHERE evaluationroom.candidatotestdetalle.idcandidato = :idcandidate \
                AND evaluationroom.candidatotestdetalle.idtestpsicologico = :idtestpsicologico '''
                
            db.execute(text(sql_query), data)
            db.execute(text(sql_insert_detail), data)
            db.execute(text(sql_update), data)
            db.execute(text(sql_delete), data)
        
            db.commit()

            logger.debug("Reset.", idcandidato=idcandidate, idtestpsicologico=idpsychologicaltest, times=times)
            result, flag, message = times, True, 'Se reseteó la prueba en base de datos.'
        except Exception as e:
            logger.error("Error.", idcandidato=idcandidate, idtestpsicologico=idpsychologicaltest, error=e)
            db.rollback()
            flag, message = False, f'Hubo un error al resetear la prueba en base de datos {e}'
        finally:
            logger.debug("Reset.", message=message)
            return flag, message, result
