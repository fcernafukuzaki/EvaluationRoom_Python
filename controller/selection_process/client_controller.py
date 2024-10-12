from datetime import datetime
from flask import request
from flask_restful import Resource
from configs.resources import app
from common.util import field_in_dict, get_response_body, str2bool
from service.authorizer_service import AuthorizerService
from service.selection_process.client_service import ClientService

authorizer_service = AuthorizerService()
client_service = ClientService()

class ClientController(Resource):
    
    def get(self, uid=None):
        response_body, code, message = None, 403, 'Operación inválida.'
        user_message = message
        try:
            token = request.headers['Authorization']
            email = request.headers['correoElectronico']

            flag, respuesta, codigo, _ = authorizer_service.validate_recruiter_identify(token, email)
            if flag:
                if not uid:
                    result, code, message = client_service.get_clients()
                    response_body = {'clients':result} if result else None
                else:
                    result, code, message = client_service.get_client(uid)
                    response_body = {'client':result} if result else None
                user_message = message
        except Exception as e:
            print(message)
            code, message = 503, f'Hubo un error al consultar clientes {e}'
            user_message = message
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), code
    
    def post(self):
        response_body, code, message = None, 403, 'Operación inválida.'
        user_message = message
        try:
            token = request.headers['Authorization']
            email = request.headers['correoElectronico']

            flag, respuesta, codigo, _ = authorizer_service.validate_recruiter_identify(token, email)
            if flag:
                input_json = request.json
                nombre = input_json['nombre'] if field_in_dict(input_json, 'nombre') else None
                
                result, code, message = client_service.add_client(nombre)
                response_body = {'client':result} if result else None
                user_message = message
        except Exception as e:
            code, message = 503, f'Hubo un error al guardar cliente {e}'
            user_message = message
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), code

    def put(self):
        response_body, code, message = None, 403, 'Operación inválida.'
        user_message = message
        try:
            token = request.headers['Authorization']
            email = request.headers['correoElectronico']

            flag, respuesta, codigo, _ = authorizer_service.validate_recruiter_identify(token, email)
            if flag:
                input_json = request.json
                idclient = input_json['idclient'] if field_in_dict(input_json, 'idclient') else None
                nombre = input_json['nombre'] if field_in_dict(input_json, 'nombre') else None
                
                result, code, message = client_service.update_client(idclient, nombre)
                user_message = message

                response_body = {'client':{'uid':result, 'datetime':datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")}} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al actualizar cliente {e}'
            user_message = message
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), code

    def delete(self):
        response_body, code, message = None, 403, 'Operación inválida.'
        user_message = message
        try:
            token = request.headers['Authorization']
            email = request.headers['correoElectronico']

            flag, respuesta, codigo, _ = authorizer_service.validate_recruiter_identify(token, email)
            if flag:
                input_json = request.json
                idclient = input_json['idclient'] if field_in_dict(input_json, 'idclient') else None
                
                result, code, message = client_service.delete_client(idclient)
                user_message = message

                response_body = {'client':{'uid':result, 'datetime':datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")}} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al eliminar cliente {e}'
            user_message = message
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), code