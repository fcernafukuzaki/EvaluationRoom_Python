from flask import jsonify, request
from flask_restful import Resource
from common.util import get_response_body
from service.authorizer_service import AuthorizerService
from service.candidate_form.psychologicaltest_service import PsychologicalTestService

authorizer_service = AuthorizerService()
psychologicaltest_service = PsychologicalTestService()

class PsychologicalTestController(Resource):

    def get(self):
        token = request.headers['Authorization']
        validated = authorizer_service.validate_token(token)
        if validated:
            result, code, message = psychologicaltest_service.get_psychologicaltests()
            response_body = {'psychologicaltests':result} if result else None
            
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=message), 404
        message = 'Operación inválida.'
        user_message = 'Operación inválida.'
        return get_response_body(code=403, message=message, user_message=user_message), 403