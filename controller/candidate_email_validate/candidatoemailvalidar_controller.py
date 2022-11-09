from flask import request
from flask_restful import Resource
from configs.flask_config import app
from service.candidate_email_validate.candidatoemailvalidar_service import CandidatoEmailValidarService
from service.authorizer_service import AuthorizerService

candidatoemailvalidar_service = CandidatoEmailValidarService()
autorizador_service = AuthorizerService()

class CandidatoEmailValidarController(Resource):

    def get(self):
        email_candidato = request.headers['Authorization']
        valido = autorizador_service.validate_token(email_candidato)
        if valido:
            return candidatoemailvalidar_service.valida_email(email_candidato)
        return {'mensaje': 'Operación no valida.'}, 403
