from flask import jsonify, request
from flask_restful import Resource
from common.util import get_response_body
from service.authorizer_service import AuthorizerService
from service.menu.psychologicaltests_service import PsychologicalTestsService

authorizer_service = AuthorizerService()
psychologicaltests_service = PsychologicalTestsService()

class PsychologicalTestsController(Resource):

    def get(self, email):
        token = request.headers['Authorization']

        flag, respuesta, codigo, id_user = authorizer_service.validate_recruiter_identify(token, email)
        if flag:
            result, code, message = psychologicaltests_service.get_psychologicaltests()
            response_body = {'psychologicaltests':result} if result else None
            
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=message), 404
        message = 'Operación inválida.'
        user_message = 'Operación inválida.'
        return get_response_body(code=403, message=message, user_message=user_message), 403