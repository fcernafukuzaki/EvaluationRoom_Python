from flask import jsonify, request
from flask_restful import Resource
from common.util import get_response_body
from service.authorizer_service import AuthorizerService
from service.candidate_form.country_service import CountryService
from service.candidate_form.departamento_service import DepartamentoService
from service.candidate_form.provincia_service import ProvinciaService
from service.candidate_form.distrito_service import DistritoService

authorizer_service = AuthorizerService()
country_service = CountryService()
departamento_service = DepartamentoService()
provincia_service = ProvinciaService()
distrito_service = DistritoService()

class UbigeoController(Resource):

    def get(self, idcountry=None, iddepartamento=None, idprovincia=None):
        token = request.headers['Authorization']
        validated = authorizer_service.validate_token(token)
        if validated:
            if not idcountry:
                result, code, message = country_service.get_countries()
                response_body = {'paises':result} if result else None
                
            if idcountry and not iddepartamento:
                result, code, message = departamento_service.get_departamentos_by_country(idcountry)
                response_body = {'departamentos':result} if result else None
                
            if idcountry and iddepartamento and not idprovincia:
                result, code, message = provincia_service.get_provincias_by_ids(idcountry,iddepartamento)
                response_body = {'provincias':result} if result else None
                
            if idcountry and iddepartamento and idprovincia:
                result, code, message = distrito_service.get_distritos_by_ids(idcountry,iddepartamento,idprovincia)
                response_body = {'distritos':result} if result else None
            
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=message), 404
        message = 'Operación inválida.'
        user_message = 'Operación inválida.'
        return get_response_body(code=403, message=message, user_message=user_message), 403