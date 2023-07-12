from flask import request
from flask_restful import Resource
# from configs.resources import app
# from service.selectionprocess_service import SelectionProcessService
from admin.authorizer_service import AuthorizerService

# selectionprocess_service = SelectionProcessService()
authorizer_service = AuthorizerService()

class CandidateWithoutSelectionProcessController(Resource):
    
    def post(self):
        token = request.json['headers']['Authorization']
        email = request.json['headers']['correoelectronico']
        flag, respuesta, codigo, _ = authorizer_service.validate_recruiter_identify(token, email)
        if flag:
            # return selectionprocess_service.get_candidates_without_selectionprocess()
            #
            return None
        return {'message': respuesta}, codigo
