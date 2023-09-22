import json
import pandas as pd
from datetime import datetime, timezone
from configs.resources import db, text
from configs.logging import logger
from repository.candidate_repository import CandidateRepository
from controller.candidate_form.candidate_service import CandidateService


candidate_service = CandidateService()
candidaterepository = CandidateRepository()


class CandidateEvaluationService():

    def registrar_log(self, token, uid, idtestpsicologico, idparte, flag, origin, host, user_agent):
        result = None
        try:
            if token:
                data = str(token).lower()
                result_val, code, message = candidate_service.get_by_email(data)
                
                if result_val is None:
                    result_val, code, message = candidate_service.get_by_document(data)
                
                    if result_val is None:
                        code, message = 404, 'No existe candidato.'
                        return result_val, code, message
                
                idcandidato = result_val.get("idcandidato")
                result_val, flag, message = self.registrar_log_candidato(idcandidato, idtestpsicologico, idparte, flag, origin, host, user_agent)
                
                if flag == False:
                    accion_aux = 'Fin de Prueba' if flag == 'F' else 'Inicio de Prueba'
                    accion = f'Error al registrar {accion_aux} del candidato {idcandidato} ({token})'
                    detalle = f'Candidato: {idcandidato} ({token}). Datos de prueba: {idtestpsicologico}.{idparte}'
                    _ = self.insert_log(idcandidato, accion, detalle, origin, host, user_agent)
                
                
                obj_data = {"mensaje": result_val} if result_val else None

                if flag:
                    result, code, message = obj_data, 200, 'Se encontró candidato.'
                else:
                    code, message = 404, 'No existe candidato.'
        except Exception as e:
            accion = f'Error al registrar respuesta del candidato {idcandidato}'
            detalle = f'Candidato: {idcandidato}. Datos de la pregunta: {idtestpsicologico}.{idparte}.'
            _ = self.insert_log(idcandidato, accion, detalle, origin, host, user_agent)
            
            code, message = 503, f'Hubo un error al obtener datos de los candidato en base de datos {e}'
        finally:
            logger.info("Response from candidato.", uid=uid, message=message)
            return result, code, message
   

    def registrar_respuesta(self, token, uid, idtestpsicologico, idparte, idpregunta, respuesta, origin, host, user_agent):
        """ 
        Descripción:
            Registrar la respueta de un candidato.
        Input:
            - uid:int Identificador del candidato.
        Output:
            - data: Objeto de datos del candidato.
        """
        result = None
        try:
            if token:
                data = str(token).lower()
                result_val, code, message = candidate_service.get_by_email(data)
                
                if result_val is None:
                    result_val, code, message = candidate_service.get_by_document(data)
                
                    if result_val is None:
                        code, message = 404, 'No existe candidato.'
                        return result_val, code, message
                
                idcandidato = result_val.get("idcandidato")
                result_val, flag, message = self.insert_answer(idcandidato, idtestpsicologico, idparte, 
                            idpregunta, respuesta, origin, 
                            host, user_agent)
                
                
                obj_data = {"mensaje": result_val} if result_val else None

                if flag:
                    result, code, message = obj_data, 200, 'Se encontró candidato.'
                else:
                    code, message = 404, 'No existe candidato.'
        except Exception as e:
            accion = f'Error al registrar respuesta del candidato {idcandidato}'
            detalle = f'Candidato: {idcandidato}. Datos de la pregunta: {idtestpsicologico}.{idparte}.{idpregunta}. Respuesta: {json.dumps(respuesta)}'
            _ = self.insert_log(idcandidato, accion, detalle, origin, host, user_agent)
            
            code, message = 503, f'Hubo un error al obtener datos de los candidato en base de datos {e}'
        finally:
            logger.info("Response from candidato.", uid=uid, message=message)
            return result, code, message


    def insert_answer(self, idcandidato:int, idtestpsicologico:int, idparte:int, 
                            idpregunta:int, respuesta:str, origin:str, 
                            host:str, user_agent:str):
        try:
            date_login = datetime.now(timezone.utc)
            respuesta_string = json.dumps(respuesta)

            sql_query = f"""
            INSERT INTO evaluationroom.candidatotestdetalle
            (idcandidato, idtestpsicologico, idparte, idpregunta, respuesta, fecharegistro, origin, host, user_agent)
            VALUES 
            ({idcandidato}, {idtestpsicologico}, {idparte}, {idpregunta}, '{respuesta_string}', '{date_login}',
            '{origin}', '{host}', '{user_agent}')
            """
            
            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))
            db.commit()
            
            result, flag, message = 'Registro exitoso.', True, 'Se registró datos del candidato.'
        except Exception as e:
            db.rollback()
            result, flag, message = 0, False, f'Hubo un error al registrar datos del candidato en base de datos {e}'
        finally:
            logger.info("Datos del candidato inserted.", uid=idcandidato, message=message)
            return result, flag, message
    
    
    def registrar_log_candidato(self, idcandidato, idtestpsicologico, idparte, flag, origin, host, user_agent):
        ''' Si el valor del argumento flag es 'F', 
                entonces buscar si existe registro previo y actualizar la fecha de fin
                e invocar API de interpretación de resultados
            Si el valor del argumento flag es diferente a 'F',
                entonces insertar nuevo registro con fecha de inicio
        '''
        try:
            if flag == 'F':
                sql_query = f"""
                SELECT idcandidato
                FROM evaluationroom.candidatotest_log
                WHERE idcandidato={idcandidato}
                AND idtestpsicologico={idtestpsicologico}
                AND idparte={idparte}
                ORDER BY fechainicio DESC
                """

                response_database = db.execute(text(sql_query))

                if int(response_database.rowcount) > 0:
                    fechainicio = response_database.fetchone().fechainicio

                    fechafin = datetime.now(timezone.utc)
                    sql_query = f"""
                    UPDATE evaluationroom.candidatotest_log
                    SET fechafin='{fechafin}'
                    WHERE idcandidato={idcandidato}
                    AND idtestpsicologico={idtestpsicologico}
                    AND idparte={idparte}
                    AND fechainicio='{fechainicio}'
                    """
                    
                    # Ejecutar la consulta SQL y obtener los resultados en un dataframe
                    response_database_update = db.execute(text(sql_query))
                    db.commit()

                    try:
                        ## Interpretar resultados
                        # psychologicaltestinterpretacion_service.getinterpretacion(idcandidato)
                        pass
                    except:
                        print('Error al interpretar los resultados del candidato {}.'.format(idcandidato))

                    return True, 'Actualización exitosa.'


            fechainicio = datetime.now(timezone.utc)

            sql_query = f"""
            INSERT INTO evaluationroom.candidatotest_log
            (idcandidato, idtestpsicologico, idparte, fechainicio, origin, host, user_agent)
            VALUES 
            ({idcandidato}, {idtestpsicologico}, {idparte}, '{fechainicio}',
            '{origin}', '{host}', '{user_agent}')
            """
            
            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))
            db.commit()
            
            result, flag, message = 'Registro exitoso.', True, 'Se registró datos del candidato.'
        except Exception as e:
            db.rollback()
            result, flag, message = 0, False, f'Hubo un error al registrar acción del candidato en base de datos {e}'
        finally:
            logger.info("Datos del candidato inserted.", uid=idcandidato, message=message)
            return result, flag, message

    
    def insert_log(self, idcandidato:int, accion:str, detalle:str,
               origin:str, host:str, user_agent:str):
        try:
            fecharegistro = datetime.now(timezone.utc)

            sql_query = f"""
            INSERT INTO evaluationroom.candidato_log
            (fecharegistro, idcandidato, accion, detalle, origin, host, user_agent)
            VALUES 
            ({fecharegistro}, {idcandidato}, {accion}, {detalle},
            '{origin}', '{host}', '{user_agent}')
            """
            
            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))
            db.commit()
            
            result, flag, message = 'Registro exitoso.', True, 'Se registró datos del candidato.'
        except Exception as e:
            db.rollback()
            result, flag, message = 0, False, f'Hubo un error al registrar acción del candidato en base de datos {e}'
        finally:
            logger.info("Datos del candidato inserted.", uid=idcandidato, message=message)
            return result, flag, message
