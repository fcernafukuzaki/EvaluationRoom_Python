from flask_restful import Resource
from common.util import get_response_body
from .estado_civil_service import EstadoCivilService


estado_civil_service = EstadoCivilService()


class EstadoCivilController(Resource):

    def get(self):
        """ Obtener estados civil.
        """
        response_body = None
        try:
            result, code, message = estado_civil_service.get_estados_civil()
            response_body = {'estados_civil':result} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al consultar estados civil {e}'
            user_message = message
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), 404
