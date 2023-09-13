from configs.logging import logger
from repository.mensaje_procesoseleccion_candidato_repository import EvaluationMessageCandidateRepository


evaluationmessagecandidate_repository = EvaluationMessageCandidateRepository()


class MensajeProcesoseleccionCandidatoService:

    def obtener_mensajes_error(self, type):
        """Obtener los mensajes de error."""
        result = None
        try:
            flag, message, result = evaluationmessagecandidate_repository.get_mensajes_error(type)
            code = 200 if flag else 404
        except Exception as e:
            code, message = 503, f"Hubo un error al obtener datos de mensajes de error en base de datos {e}",
        finally:
            logger.info(message)
            return result, code, message


    def mensaje_bienvenida(self, nombre, uid=1):
        """Obtener el mensaje de bienvenida."""
        result = None
        try:
            code, message, objeto = evaluationmessagecandidate_repository.get_mensaje_bienvenida(uid)
            
            # Colocar el nombre del candidato en el mensaje de bienvenida.
            result = objeto.get("mensaje").format(nombre)
        except Exception as e:
            code, message = False, f"Hubo un error al obtener datos de mensaje de bienvenida en base de datos {e}",
        finally:
            logger.info('El candidato {} va a iniciar el examen (mensaje de bienvenida)'.format(nombre), code=code)
            return result, code, message
