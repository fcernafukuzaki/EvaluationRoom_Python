from configs.logging import logger
from soporte_tecnico.repository.soportetecnico_notificacion_repository import SoporteTecnicoNotificacionRepository


soportetecniconotificacion_repository = SoporteTecnicoNotificacionRepository()


class SoporteTecnicoNotificacionService():

    def guardar_mensaje_error_candidato(self, correo_electronico:str, observacion:str, detalle=None):
        """
        Descripción:
            Agregar un mensaje de error ocurrido durante la evaluación.
        Input:
            - correo_electronico:str Correo electrónico del candidato.
            - observacion:str Mensaje de error ocurrido.
            - detalle:str Detalle del error ocurrido.
        
        Output:
            - result:object Valor 1 si se registró la notificación.
            - code:int Código de respuesta. [200:OK, 404:Not Found, 503:Error]
            - message:str Mensaje de salida.
        """
        result = None
        try:
            flag, message, result = soportetecniconotificacion_repository.add(correo_electronico, observacion, detalle)
            code = 200 if flag else 404
        except Exception as e:
            code, message = 503, f'Error al registrar notificación de error. {e}'
        finally:
            logger.debug("Notificación del error inserted.", message=message)
            return result, code, message
