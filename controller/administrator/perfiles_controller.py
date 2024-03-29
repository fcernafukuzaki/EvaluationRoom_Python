from flask import jsonify, request
from flask_restful import Resource
from common.util import field_in_dict, get_response_body, str2bool
from service.authorizer_service import AuthorizerService
from service.administrator.perfiles_service import PerfilesService

authorizer_service = AuthorizerService()
perfiles_service = PerfilesService()

class PerfilesController(Resource):

    def get(self, uid=None):
        response_body = None
        try:
            token = request.headers['Authorization']
            email = request.headers['correoElectronico']

            flag, respuesta, codigo, _ = authorizer_service.validate_recruiter_identify(token, email)
            if flag:
                if not uid:
                    result, code, message = perfiles_service.get_perfiles()
                    response_body = {'perfiles':result} if result else None
                else:
                    result, code, message = perfiles_service.get_perfil(uid)
                    response_body = {'perfil':result} if result else None
                user_message = message
            else:
                code, message = 403, 'Operación inválida.'
                user_message = message
        except Exception as e:
            code, message = 503, f'Hubo un error al consultar perfiles {e}'
            user_message = message
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), code
    
    def post(self):
        response_body = None
        try:
            token = request.headers['Authorization']
            email = request.headers['correoElectronico']

            flag, respuesta, codigo, _ = authorizer_service.validate_recruiter_identify(token, email)
            if flag:
                input_json = request.json
                nombre = input_json['nombre'] if field_in_dict(input_json, 'nombre') else None

                result, code, message = perfiles_service.add_perfil(nombre)
                response_body = {'perfil':result} if result else None
            else:
                code, message = 403, 'Operación inválida.'
            user_message = message
        except Exception as e:
            code, message = 503, f'Hubo un error al guardar perfil {e}'
            user_message = message
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), code
    
    def put(self, uid):
        response_body = None
        try:
            token = request.headers['Authorization']
            email = request.headers['correoElectronico']

            flag, respuesta, codigo, _ = authorizer_service.validate_recruiter_identify(token, email)
            if flag:
                input_json = request.json
                idperfil = input_json['idPerfil'] if field_in_dict(input_json, 'idPerfil') else None
                nombre = input_json['nombre'] if field_in_dict(input_json, 'nombre') else None

                result, code, message = perfiles_service.update_perfil(uid, nombre)
                response_body = {'perfil':result} if result else None
            else:
                code, message = 403, 'Operación inválida.'
            user_message = message
        except Exception as e:
            code, message = 503, f'Hubo un error al actualizar perfil {e}'
            user_message = message
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), code
