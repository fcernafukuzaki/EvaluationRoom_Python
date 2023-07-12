from flask import request
from flask_restful import Resource
# from datetime import datetime
# from common.util import field_in_dict, get_response_body, str2bool
from .authorizer_service import AuthorizerService
from .usuarios_service import UsuariosService
from common.util import get_response_body
from configs.logging import logger

authorizer_service = AuthorizerService()
usuarios_service = UsuariosService()

class UsuariosController(Resource):

    def get(self, uid=None):
        """ Obtener datos de los usuarios o de un usuario.
        Header:
            - Authorization: Valor retornado por API de Login.
            - correoElectronico: Correo electrónico del usuario que intenta acceder.
        """
        response_body = None
        try:
            input_header = request.headers
            token = input_header.get('Authorization')
            correoelectronico = input_header.get('correoElectronico')
            
            flag, respuesta, codigo, _ = authorizer_service.validate_recruiter_identify(token, correoelectronico)
            logger.debug("Response from validate recruiter.", respuesta=respuesta, codigo=codigo)
            if flag:
                if not uid:
                    result, code, message = usuarios_service.get_usuarios()
                    response_body = {'usuarios':result} if result else None
                else:
                    result, code, message = usuarios_service.get_usuario(uid)
                    response_body = {'usuario':result} if result else None
                user_message = message
            else:
                code, message = 403, 'Operación inválida.'
                user_message = message
        except Exception as e:
            code, message = 503, f'Hubo un error al consultar usuarios {e}'
            user_message = message
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), code
    
    # def post(self):
    #     response_body = None
    #     try:
    #         token = request.headers['Authorization']
    #         email = request.headers['correoElectronico']

    #         flag, respuesta, codigo, _ = authorizer_service.validate_recruiter_identify(token, email)
    #         if flag:
    #             input_json = request.json
    #             nombre = input_json['nombre'] if field_in_dict(input_json, 'nombre') else None
    #             correoelectronico = input_json['correoElectronico'] if field_in_dict(input_json, 'correoElectronico') else None
    #             activo = input_json['activo'] if field_in_dict(input_json, 'activo') else None
    #             perfiles = input_json['perfiles'] if field_in_dict(input_json, 'perfiles') else None

    #             result, code, message = usuarios_service.add_usuario(nombre, correoelectronico, activo, perfiles)
    #             response_body = {'usuario':result} if result else None
    #             user_message = message
    #         else:
    #             code, message = 403, 'Operación inválida.'
    #             user_message = 'Operación inválida.'
    #     except Exception as e:
    #         code, message = 503, f'Hubo un error al guardar usuario {e}'
    #         user_message = message
    #     finally:
    #         if response_body:
    #             return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
    #         return get_response_body(code=code, message=message, user_message=user_message), code
    
    # def put(self, uid):
    #     response_body = None
    #     try:
    #         token = request.headers['Authorization']
    #         email = request.headers['correoElectronico']

    #         flag, respuesta, codigo, _ = authorizer_service.validate_recruiter_identify(token, email)
    #         if flag:
    #             input_json = request.json
    #             idusuario = input_json['idUsuario'] if field_in_dict(input_json, 'idUsuario') else None
    #             nombre = input_json['nombre'] if field_in_dict(input_json, 'nombre') else None
    #             correoelectronico = input_json['correoElectronico'] if field_in_dict(input_json, 'correoElectronico') else None
    #             activo = input_json['activo'] if field_in_dict(input_json, 'activo') else None
    #             perfiles = input_json['perfiles'] if field_in_dict(input_json, 'perfiles') else None

    #             result, code, message = usuarios_service.update_usuario(uid, nombre, correoelectronico, activo, perfiles)
                
    #             user_message = message
    #             if not perfiles:
    #                 resultado, code, message = usuarios_service.get_usuario(idusuario)
    #                 perfiles_eliminar = [t["idperfil"] for t in resultado["perfiles"]]
    #                 _, code, message = usuarios_service.delete_perfiles(idusuario, perfiles_eliminar)
    #                 user_message = f"{user_message} {message}"
    #             if perfiles:
    #                 resultado, code, message = usuarios_service.get_usuario(idusuario)
    #                 idperfiles_original = [t["idperfil"] for t in resultado["perfiles"]]
    #                 perfiles_nuevo = [t for t in perfiles if t not in idperfiles_original]
    #                 perfiles_eliminar = [t for t in idperfiles_original if t not in perfiles]
                    
    #                 _, code, message = usuarios_service.delete_perfiles(idusuario, perfiles_eliminar)
    #                 user_message = f"{user_message} {message}"
                    
    #                 _, code, message = usuarios_service.add_perfiles(idusuario, perfiles_nuevo)
    #                 user_message = f"{user_message} {message}"
                
    #             response_body = {'usuario':{'uid':result, 'datetime':datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")}} if result else None
    #         else:
    #             code, message = 403, 'Operación inválida.'
    #         user_message = message
    #     except Exception as e:
    #         code, message = 503, f'Hubo un error al actualizar usuario {e}'
    #         user_message = message
    #     finally:
    #         if response_body:
    #             return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
    #         return get_response_body(code=code, message=message, user_message=user_message), code
