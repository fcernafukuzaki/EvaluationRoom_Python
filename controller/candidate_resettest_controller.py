from flask import request
from flask_restful import Resource
from common.util import get_response_body
from common.validate_handler import authorize_user
from service.candidate_resettest_service import CandidateResetTestService
from authorization.usuario_validar_service import UsuarioValidarService


usuariovalidar_service = UsuarioValidarService()
candidate_resettest_service = CandidateResetTestService()


class CandidateResetTestController(Resource):
    
    @authorize_user
    def post(self):
        """ Reset de las preguntas respondidas por un candidato en un test psicológico.
        """
        response_body = None
        try:
            input_header = request.headers
            email = input_header.get('correoElectronico')

            email_valido, mensaje, usuario = usuariovalidar_service.get_data(email)
            if email_valido:
                id_user = usuario.get("idusuario")

                input_json = request.json
                idcandidate = input_json.get('idcandidate')
                idpsychologicaltest = input_json.get('idpsychologicaltest')
            
                result, code, message = candidate_resettest_service.reset_candidate_test(id_user, idcandidate, idpsychologicaltest)
                response_body = {'message':result} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al resetear test {e}'
        finally:
            user_message = message
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), code
