from flask import request
from flask_restful import Resource
from configs.flask_config import app
from service.soporte_tecnico.mensaje_procesoseleccion_candidato_service import MensajeProcesoseleccionCandidatoService
from service.soporte_tecnico.soportetecnico_notificacion_service import SoporteTecnicoNotificacionService
from service.apigateway_notificacion_service import APIGatewayNotificacionService
from service.authorizer_service import AuthorizerService

mensaje_procesoseleccion_candidato_service = MensajeProcesoseleccionCandidatoService()
soportetecnico_notificacion_service = SoporteTecnicoNotificacionService()
apigateway_notificacion_service = APIGatewayNotificacionService()
autorizador_service = AuthorizerService()

class CandidatoSoporteTecnicoNotificacionController(Resource):

    def get(self):
        email_candidato = request.headers['Authorization']
        valido = autorizador_service.validate_token(email_candidato)
        if valido:
            return mensaje_procesoseleccion_candidato_service.obtener_mensajes_error()
        return {'mensaje': 'Operación no valida.'}, 403
    
    def post(self):
        email_candidato = request.headers['Authorization']
        valido = autorizador_service.validate_token(email_candidato)
        if valido:
            json_dict = request.json
            if json_dict is not None:
                if 'correo_electronico' in json_dict:
                    correo_electronico = request.json['correo_electronico']
                    observacion = request.json['observacion']
                    detalle = request.json['detalle']
                    flag, mensaje = soportetecnico_notificacion_service.guardar_mensaje_error_candidato(correo_electronico, observacion, detalle)
                    if flag:
                        flag, _ = apigateway_notificacion_service.notificar_error(correo_electronico, observacion, detalle)
                        return {'mensaje': mensaje}, 200
                    return {'mensaje': mensaje}, 500
        return {'mensaje': 'Operación no valida.'}, 403
