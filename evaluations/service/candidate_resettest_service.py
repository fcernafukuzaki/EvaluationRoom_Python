from configs.logging import logger
from evaluations.repository.candidate_resettest_service_repository import CandidateResetTestRepository


candidateresettest_repository = CandidateResetTestRepository()


class CandidateResetTestService():
    """
    Reset de preguntas de una prueba psicológica.
    """
    def reset_candidate_test(self, id_user, idcandidate, idpsychologicaltest):
        """
        Descripción:
            Resetear las preguntas de un test psicológico asignado a un candidato/paciente.
        Input:
            - id_user: Identificador del usuario.
            - idcandidate: Identificador del candidato.
            - idpsychologicaltest: Identificador del test psicológico.
        Output:
            - result: Objeto.
            - code: Código de respuesta. [200:OK, 503:Error]
            - message: Mensaje de salida.
        """
        result = None
        times = 0
        try:
            flag, message, times_reseted = candidateresettest_repository.count_tries(idcandidate, idpsychologicaltest)
            if flag:
                times = times_reseted + 1

            flag, message, result = candidateresettest_repository.reset(id_user, idcandidate, idpsychologicaltest, times)
            
            logger.debug("Test reseted.", times_reseted=times_reseted)
            result, code, message = times_reseted, 200, 'Se reseteó la prueba en base de datos.'
        except Exception as e:
            logger.error("Error.", error=e)
            code, message = 503, f'Hubo un error al resetear la prueba en base de datos {e}'
        finally:
            logger.debug("Test reseted.", message=message)
            return result, code, message
