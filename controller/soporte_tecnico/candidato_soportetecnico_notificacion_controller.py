from flask import request
from flask_restful import Resource
from common.util import get_response_body
from common.validate_handler import authorize_candidate
from .mensaje_procesoseleccion_candidato_service import MensajeProcesoseleccionCandidatoService
from .soportetecnico_notificacion_service import SoporteTecnicoNotificacionService
from .apigateway_notificacion_service import APIGatewayNotificacionService


mensaje_procesoseleccion_candidato_service = MensajeProcesoseleccionCandidatoService()
soportetecnico_notificacion_service = SoporteTecnicoNotificacionService()
apigateway_notificacion_service = APIGatewayNotificacionService()


class CandidatoSoporteTecnicoNotificacionController(Resource):

    @authorize_candidate
    def get(self):
        """ Obtener los tipos de errores.
        """
        response_body = None
        try:
            result, code, message = mensaje_procesoseleccion_candidato_service.obtener_mensajes_error()
            response_body = {'mensajes':result} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al consultar mensajes de error {e}'
        finally:
            user_message = message
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), code


    @authorize_candidate
    def post(self):
        """ Guardar el error reportado por un candidato/paciente.
        """
        response_body = None
        try:
            data = request.json
            if data is not None:
                correo_electronico = data.get('correo_electronico')
                observacion = data.get('observacion')
                detalle = data.get('detalle')
                flag, code, message = soportetecnico_notificacion_service.guardar_mensaje_error_candidato(correo_electronico, observacion, detalle)
                if flag:
                    flag, _ = apigateway_notificacion_service.notificar_error(correo_electronico, observacion, detalle)
                response_body = {'mensaje':message} if message else None
        except Exception as e:
            code, message = 503, f'Hubo un error al registrar mensaje de error {e}'
        finally:
            user_message = message
            if response_body:
                return get_response_body(code=201, message='OK', user_message=message, body=response_body), 201
            return get_response_body(code=code, message=message, user_message=user_message), code
