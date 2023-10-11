from flask import request
from flask_restful import Resource
from common.util import get_response_body, obtener_header
from common.validate_handler import authorize_candidate
from controller.candidate_evaluation.candidate_evaluation_service import CandidateEvaluationService
from .evaluation_service import EvaluationService


candidate_evaluation_service = CandidateEvaluationService()
evaluation_service = EvaluationService()


class RespuestaController(Resource):
    
    @authorize_candidate
    def post(self):
        """ Obtener los datos del candidato a partir de su correo electrónico o número de documento de identidad.
        """
        response_body = None
        try:
            input_header = request.headers
            data = input_header.get('Authorization')
            data_json = request.json
            data_json = data_json.get("guardarCandidatoTestPsicologicoRespuesta")
            
            if data and data_json and 'idcandidato' in data_json:
                idcandidato, idtestpsicologico, idparte, idpregunta, respuesta = (
                    data_json['idcandidato'], 
                    data_json['idtestpsicologico'], 
                    data_json['idparte'], 
                    data_json['idpregunta'], 
                    data_json['respuesta']
                )

                origin, host, user_agent = obtener_header(request.headers)
                
                result, code, message = candidate_evaluation_service.registrar_respuesta(data, idcandidato, idtestpsicologico, idparte, idpregunta, respuesta, origin, host, user_agent)
                response_body = {"evaluations": result} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al consultar las evaluaciones {e}'
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=message), 404
        