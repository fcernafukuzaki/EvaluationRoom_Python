from flask_restful import Resource
from common.util import get_response_body
from .sexo_service import SexoService


sexo_service = SexoService()


class SexoController(Resource):

    def get(self):
        """ Obtener géneros.
        """
        response_body = None
        try:
            result, code, message = sexo_service.get_sexos()
            response_body = {'sexo':result} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al consultar género {e}'
            user_message = message
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), 404
