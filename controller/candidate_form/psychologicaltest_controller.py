from flask_restful import Resource
from common.util import get_response_body
from .psychologicaltest_service import PsychologicalTestService


psychologicaltest_service = PsychologicalTestService()


class PsychologicalTestController(Resource):

    def get(self):
        """ Obtener tests psicológicos.
        """
        response_body = None
        try:
            result, code, message = psychologicaltest_service.get_psychologicaltests()
            response_body = {'psychologicaltests':result} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al consultar tests psicológicos {e}'
        finally:
            user_message = message
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), 404
