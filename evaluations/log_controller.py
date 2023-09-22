from flask import request
from flask_restful import Resource
from common.util import get_response_body
from common.validate_handler import authorize_candidate
from controller.candidate_evaluation.candidate_evaluation_service import CandidateEvaluationService
from .evaluation_service import EvaluationService
from authorization.authorizer_service import AuthorizerService


candidate_evaluation_service = CandidateEvaluationService()
evaluation_service = EvaluationService()
authorizer_service = AuthorizerService()


class LogController(Resource):
    
    @authorize_candidate
    def post(self):
        """ Obtener los datos del candidato a partir de su correo electrónico o número de documento de identidad.
        """
        response_body = None
        try:
            input_header = request.headers
            data = input_header.get('Authorization')
            data_json = request.json

            data_json = data_json.get("guardarCandidatoTestPsicologicoLog")
            if data and data_json and 'idcandidato' in data_json:
                idcandidato, idtestpsicologico, idparte, flag = (
                    data_json['idcandidato'], 
                    data_json['idtestpsicologico'], 
                    data_json['idparte'], 
                    data_json['flag']
                )

                origin, host, user_agent = authorizer_service.obtener_header(request.headers)
                
                result, code, message = candidate_evaluation_service.registrar_log(data, idcandidato, idtestpsicologico, idparte, flag, origin, host, user_agent)
                response_body = {"evaluations": result} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al consultar las evaluaciones {e}'
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=message), 404
        