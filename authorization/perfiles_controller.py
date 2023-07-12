from flask import jsonify, request
from flask_restful import Resource
from common.util import get_response_body
from common.validate_handler import authorize_user
from .perfiles_service import PerfilesService

perfiles_service = PerfilesService()

class PerfilesController(Resource):

    @authorize_user
    def get(self, uid=None):
        """ Obtener datos de los perfiles.
        Header:
            - Authorization: Valor retornado por API de Login.
            - correoElectronico: Correo electrónico del usuario que intenta acceder.
        """
        response_body = None
        try:
            if not uid:
                result, code, message = perfiles_service.get_perfiles()
                response_body = {'perfiles':result} if result else None
            else:
                result, code, message = perfiles_service.get_perfil(uid)
                response_body = {'perfil':result} if result else None
            user_message = message
        except Exception as e:
            code, message = 503, f'Hubo un error al consultar perfiles {e}'
            user_message = message
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), code
    
    
    @authorize_user
    def post(self):
        response_body = None
        try:
            input_json = request.json
            nombre = input_json.get('nombre')

            result, code, message = perfiles_service.add_perfil(nombre)
            response_body = {'perfil':result} if result else None
            user_message = message
        except Exception as e:
            code, message = 503, f'Hubo un error al guardar perfil {e}'
            user_message = message
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), code
    
    
    @authorize_user
    def put(self, uid):
        response_body = None
        try:
            input_json = request.json
            # idperfil = input_json.get('idPerfil')
            nombre = input_json.get('nombre')

            result, code, message = perfiles_service.update_perfil(uid, nombre)
            response_body = {'perfil':result} if result else None
            user_message = message
        except Exception as e:
            code, message = 503, f'Hubo un error al actualizar perfil {e}'
            user_message = message
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), code
