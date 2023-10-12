from flask import request
from flask_restful import Resource
from common.util import get_response_body, obtener_header
from common.validate_handler import authorize_candidate
from configs.logging import logger
from candidate.candidate_form.service.candidate_service import CandidateService
from evaluations.service.evaluation_service import EvaluationService


candidate_service = CandidateService()
evaluation_service = EvaluationService()


class EvaluationController(Resource):
    
    @authorize_candidate
    def post(self):
        """ Obtener los datos del candidato a partir de su correo electrónico o número de documento de identidad.
        """
        response_body = None
        try:
            input_header = request.headers
            data = input_header.get('Authorization')
            idempresa = input_header.get('empresa')
            origin, host, user_agent = obtener_header(request.headers)
            logger.debug("", origin=origin, host=host, user_agent=user_agent)

            if data:
                data = str(data).lower()
                result, code, message = candidate_service.get_by_email(data)
                
                if result is None:
                    result, code, message = candidate_service.get_by_document(data)
                
                    if result is None:
                        code, message = 404, 'No existe candidato.'
                        return get_response_body(code=code, message=message, user_message=message), 404
                
                idcandidato = result.get("idcandidato")
                result, code, message = evaluation_service.get(idcandidato, idempresa)
                
                response_body = {"evaluations": result} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al consultar las evaluaciones {e}'
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=message), 404
