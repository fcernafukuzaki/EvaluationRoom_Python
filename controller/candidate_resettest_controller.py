from flask import request
from flask_restful import Resource
from configs.resources import app
from service.candidate_resettest_service import CandidateResetTestService
from admin.authorizer_service import AuthorizerService

candidate_resettest_service = CandidateResetTestService()
authorizer_service = AuthorizerService()

class CandidateResetTestController(Resource):
    
    def post(self):
        token = request.json['headers']['Authorization']
        email = request.json['headers']['email']
        flag, respuesta, codigo, id_user = authorizer_service.validate_recruiter_identify(token, email)
        if flag:
            idcandidate = request.json['idcandidate']
            idpsychologicaltest = request.json['idpsychologicaltest']
            return candidate_resettest_service.reset_candidate_test(id_user, idcandidate, idpsychologicaltest)
        return {'message': respuesta}, codigo
