from flask_restful import Resource
from common.util import get_response_body
from configs.logging import logger
from psychologicalreport.api.api_test_interpretacion_service import PsychologicalTestInterpretacionService


psychologicaltestinterpretacion_service = PsychologicalTestInterpretacionService()


class PsychologicalTestInterpretacionController(Resource):
    
    def get(self, idcandidato=None, uid=None, email=None, token=None):
        """ Obtener y generar la interpretación de las pruebas psicológicas.
        """
        response_body = None
        try:
            logger.debug("PsychologicalTestInterpretacionController", idcandidato=idcandidato, uid=uid, email=email)
            
            if idcandidato:
                result, code, message = psychologicaltestinterpretacion_service.create(idcandidato)
                response_body = {"mensaje": result} if result else None
                return get_response_body(code=200, message="OK", user_message="OK", body=response_body), 200
            if uid:
                return psychologicaltestinterpretacion_service.download(uid, email, token)
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener la interpretación {e}'
            user_message = message
            return get_response_body(code=code, message=message, user_message=user_message), code
