from flask_restful import Resource
from common.util import get_response_body
from .tipo_direccion_service import TipoDireccionService


tipo_direccion_service = TipoDireccionService()


class TipoDireccionController(Resource):

    def get(self):
        """ Obtener tipos de direcciones.
        """
        response_body = None
        try:
            result, code, message = tipo_direccion_service.get_tipos_direccion()
            response_body = {'tipos_direccion':result} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al consultar tipos de direcciones {e}'
        finally:
            user_message = message
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), 404
