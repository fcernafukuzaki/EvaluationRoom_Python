from datetime import datetime
from flask import request
from flask_restful import Resource
from configs.resources import app
from common.util import field_in_dict, get_response_body, str2bool
from service.authorizer_service import AuthorizerService
from service.selection_process.jobposition_service import JobPositionService
from service.selectionprocess_service import SelectionProcessService

authorizer_service = AuthorizerService()
jobposition_service = JobPositionService()
selectionprocess_service = SelectionProcessService()

class JobPositionController(Resource):
    
    def get(self, idclient=None, idjobposition=None):
        response_body, code, message = None, 403, 'Operación inválida.'
        user_message = message
        try:
            token = request.headers['Authorization']
            email = request.headers['correoElectronico']

            flag, respuesta, codigo, _ = authorizer_service.validate_recruiter_identify(token, email)
            if flag:
                if not idjobposition:
                    result, code, message = jobposition_service.get_jobpositions(idclient)
                    response_body = {'jobpositions':result} if result else None
                else:
                    result, code, message = jobposition_service.get_jobposition(idclient, idjobposition)
                    response_body = {'jobposition':result} if result else None
                user_message = message
        except Exception as e:
            print(message)
            code, message = 503, f'Hubo un error al consultar puesto laboral {e}'
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
                idclient = input_json['idclient'] if field_in_dict(input_json, 'idclient') else None
                nombre = input_json['nombre'] if field_in_dict(input_json, 'nombre') else None
                
                result, code, message  = jobposition_service.add_jobposition(idclient, nombre)
                new_jobposition_idclient, new_jobposition_idpuestolaboral = result
                date_process_begin = request.json['date_process_begin']
                date_process_end = request.json['date_process_end']
                user_register = request.json['user_register']
                process_active = request.json['process_active']
                
                new_selectionprocess = selectionprocess_service.add_selectionprocess(idclient, new_jobposition_idpuestolaboral, date_process_begin, date_process_end, user_register, process_active)
                response_body = {'jobposition':new_jobposition_idpuestolaboral} if result else None
                user_message = message
        except Exception as e:
            code, message = 503, f'Hubo un error al guardar puesto laboral {e}'
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
                idjobposition = input_json['idjobposition'] if field_in_dict(input_json, 'idjobposition') else None
                nombre = input_json['nombre'] if field_in_dict(input_json, 'nombre') else None
                
                result, code, message = jobposition_service.update_jobposition(idclient, idjobposition, nombre)
                
                date_process_begin = request.json['date_process_begin']
                date_process_end = request.json['date_process_end']
                user_register = request.json['user_register']
                process_active = request.json['process_active']

                selectionprocess = selectionprocess_service.update_selectionprocess(idclient, idjobposition, date_process_begin, date_process_end, user_register, process_active)
                user_message = message

                response_body = {'jobposition':{'uid':result, 'datetime':datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")}} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al actualizar puesto laboral {e}'
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
                idjobposition = input_json['idjobposition'] if field_in_dict(input_json, 'idjobposition') else None
                
                result, code, message = jobposition_service.delete_jobposition(idclient, idjobposition)
                user_message = message

                response_body = {'jobposition':{'uid':result, 'datetime':datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")}} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al eliminar puesto laboral {e}'
            user_message = message
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), code