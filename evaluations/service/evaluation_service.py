from configs.logging import logger
from candidate.candidate_form.repository.candidate_repository import CandidateRepository
from candidate.candidate_form.repository.psychologicaltests_repository import PsychologicalTestsRepository
from evaluations.service.mensaje_procesoseleccion_candidato_service import MensajeProcesoseleccionCandidatoService


candidaterepository = CandidateRepository()
psychologicaltestsrepository = PsychologicalTestsRepository()
mensajeprocesoseleccionservice = MensajeProcesoseleccionCandidatoService()


class EvaluationService():
    def get(self, uid:int, idempresa:int):
        """ 
        Descripción:
            Obtener los datos de la evaluación del candidato (test, instrucciones, respuestas).
        Input:
            - uid:int Identificador del candidato.
        Output:
            - data: Objeto de datos del candidato y sus evaluaciones.
        """
        result = None
        data = dict()
        try:
            flag, message, candidato = candidaterepository.get_evaluation_by_uid(uid=uid)
            candidato_nombre = candidato.get("nombre")
            candidato = candidato if flag else {}

            flag, message, results = psychologicaltestsrepository.get_psychologicaltests_assigned(uid, idempresa)
            tests_assigned = results if flag else []
            testpsicologicos_asignados = tests_assigned

            flag, message, results = psychologicaltestsrepository.get_psychologicaltests_instructions(uid, idempresa)
            testpsicologicos_instrucciones = results.get("testpsicologicos_instrucciones") if flag else []
            preguntas_pendientes = results.get("preguntas_pendientes") if flag else []
            
            '''Si el candidato tiene pruebas asignadas y no tiene preguntas pendientes, 
            entonces el candidato ha finalizado las pruebas.
            Mostrar mensaje de felicitaciones.
            '''
            if tests_assigned and not preguntas_pendientes:
                logger.debug("No tiene preguntas pendientes.")
                result, flag_mensaje, message = mensajeprocesoseleccionservice.mensaje_felicitaciones(candidato_nombre)
                mensaje_felicitaciones = result if flag_mensaje else ""

                data = {
                    'mensaje_felicitaciones': mensaje_felicitaciones
                }
            else:
                elementos_con_fecha = list(filter(lambda x: x['fechaexamen'] is None, testpsicologicos_asignados))
                duracion_total = sum(elemento['duracionestimada'] for elemento in elementos_con_fecha)
                
                result, flag_mensaje, message = mensajeprocesoseleccionservice.mensaje_bienvenida(candidato_nombre, duracion_total)
                mensaje_bienvenida = result if flag_mensaje else ""

                data = {
                    'mensaje_bienvenida': mensaje_bienvenida,
                    'candidato': candidato,
                    'testpsicologicos_asignados': testpsicologicos_asignados,
                    'testpsicologicos_instrucciones': testpsicologicos_instrucciones,
                    'preguntas_pendientes': preguntas_pendientes
                }
            
            logger.debug("Response from evaluación.")
            result, code, message = data, 200, 'Se encontró pruebas psicológicas.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de las pruebas psicológicas en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message
