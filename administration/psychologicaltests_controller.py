from flask import request
from flask_restful import Resource
from common.util import get_response_body
from common.validate_handler import authorize_user
from .psychologicaltests_service import PsychologicalTestsService


psychologicaltests_service = PsychologicalTestsService()


class PsychologicalTestsController(Resource):

    @authorize_user
    def get(self):
        """ Obtener datos de las pruebas psicológicas.
        """
        response_body = None
        try:
            result, code, message = psychologicaltests_service.get_psychologicaltests()
            response_body = {'psychologicaltests':result} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al consultar las pruebas psicológicas {e}'
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=message), 404
