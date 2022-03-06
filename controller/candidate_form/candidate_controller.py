from flask import request
from flask_restful import Resource
from common.util import field_in_dict, get_response_body, str2bool
from service.authorizer_service import AuthorizerService
from objects.candidate import Candidate
from service.candidate_form.candidate_service import CandidateService

authorizer_service = AuthorizerService()
candidate_service = CandidateService()

class CandidateController(Resource):
    
    def get(self, uid=None, email=None):
        try:
            token = request.headers['Authorization']
            validated = authorizer_service.validate_token(token)
            if validated:
                if uid:
                    result, code, message = candidate_service.get_candidate_by_uid(uid)
                    user_message = message
                if email:
                    correoelectronico = str(email).lower()
                    result, code, message = candidate_service.get_candidate_by_email(correoelectronico)
                    user_message = message
                if result:
                    response_body = {'candidato':result} if result else None
                    return get_response_body(code=200, message='OK', user_message=user_message, body=response_body), 200
                return get_response_body(code=code, message=message, user_message=user_message), code
            message = 'Operación inválida.'
            user_message = 'Operación inválida.'
            return get_response_body(code=403, message=message, user_message=user_message), 403
        except Exception as e:
            message = f'Hubo un error al obtener datos del candidato {e}'
            return get_response_body(code=503, message=message, user_message=message), 503
    
    def post(self, self_registered="true"):
        try:
            self_register = str2bool(self_registered)
            input_json = request.json
            idcandidato = input_json['idCandidato'] if field_in_dict(input_json, 'idCandidato') else None
            idcandidato = idcandidato if isinstance(idcandidato, int) else None
            nombre = input_json['nombre'] if field_in_dict(input_json, 'nombre') else None
            apellidopaterno = input_json['apellidoPaterno'] if field_in_dict(input_json, 'apellidoPaterno') else None
            apellidomaterno = input_json['apellidoMaterno'] if field_in_dict(input_json, 'apellidoMaterno') else None
            correoelectronico = str(input_json['correoElectronico']).lower() if field_in_dict(input_json, 'correoElectronico') else None
            iddocumentoidentidad = input_json['documentoIdentidad']['idDocumentoIdentidad'] if input_json['documentoIdentidad']['idDocumentoIdentidad'] > 0 else 1
            numerodocumentoidentidad = input_json['numeroDocumentoIdentidad'] if field_in_dict(input_json, 'numeroDocumentoIdentidad') else None
            idestadocivil = input_json['estadoCivil']['idEstadoCivil'] if input_json['estadoCivil']['idEstadoCivil'] > 0 else 1
            idsexo = input_json['sexo']['idSexo'] if input_json['sexo']['idSexo'] > 0 else 1
            cantidadhijos = input_json['cantidadHijos'] if field_in_dict(input_json, 'cantidadHijos') else None
            fechanacimiento = input_json['fechaNacimiento'] if field_in_dict(input_json, 'fechaNacimiento') else None
            telefonos = input_json['telefonos'] if field_in_dict(input_json, 'telefonos') else None
            direcciones = input_json['direcciones'] if field_in_dict(input_json, 'direcciones') else None
            tests = input_json['testPsicologicos'] if field_in_dict(input_json, 'testPsicologicos') else None
            
            if not idcandidato:
                _, code, _ = candidate_service.get_candidate_by_email(correoelectronico)
                if code == 200:
                    message = f'Error relacionado a Correo electrónico.'
                    user_message = f'Ya existe un candidato con el mismo correo electrónico. Debe ingresar un email distinto.'
                    return get_response_body(code=409, message=message, user_message=user_message), 409
                
                _, code, _ = candidate_service.get_candidate_by_document(numerodocumentoidentidad)
                if code == 200:
                    message = f'Error relacionado a Número de documento.'
                    user_message = f'Ya existe un candidato con el mismo número de documento de identidad. Debe ingresar uno distinto.'
                    return get_response_body(code=409, message=message, user_message=user_message), 409

                result, code, message = candidate_service.add_candidate(idcandidato, nombre, apellidopaterno, apellidomaterno, iddocumentoidentidad, numerodocumentoidentidad, idestadocivil,
                            cantidadhijos, fechanacimiento, correoelectronico, idsexo, self_register, telefonos, direcciones)
                idcandidato = result
                user_message = message
                if idcandidato and tests:
                    result, code, message = candidate_service.add_candidate_tests(idcandidato, tests)
                    user_message = f"{user_message} {message}"
            else:
                result, code, message = candidate_service.update_candidate(idcandidato, nombre, apellidopaterno, apellidomaterno, iddocumentoidentidad, numerodocumentoidentidad, idestadocivil,
                            cantidadhijos, fechanacimiento, correoelectronico, idsexo, self_register, telefonos, direcciones)
                
                user_message = message
                if idcandidato and not tests:
                    result, code, message = candidate_service.get_candidate_by_uid(idcandidato)
                    tests_eliminar = [t["idtestpsicologico"] for t in result["psychologicaltests"]]
                    result, code, message = candidate_service.delete_candidate_tests_by_tests(idcandidato, tests_eliminar)
                    user_message = f"{user_message} {message}"
                if idcandidato and tests:
                    result, code, message = candidate_service.get_candidate_by_uid(idcandidato)
                    idtestpsicologico_original = [t["idtestpsicologico"] for t in result["psychologicaltests"]]
                    tests_nuevo = [t for t in tests if t not in idtestpsicologico_original]
                    tests_eliminar = [t for t in idtestpsicologico_original if t not in tests]
                    
                    result, code, message = candidate_service.delete_candidate_tests_by_tests(idcandidato, tests_eliminar)
                    user_message = f"{user_message} {message}"
                    
                    result, code, message = candidate_service.add_candidate_tests(idcandidato, tests_nuevo)
                    user_message = f"{user_message} {message}"

            response_body = {'candidato':{"idCandidato":idcandidato,"correoElectronico":correoelectronico}} if idcandidato else None
            return get_response_body(code=200, message='OK', user_message=user_message, body=response_body), 200
        except Exception as e:
            message = f'Hubo un error durante el registro del candidato {e}'
            return get_response_body(code=503, message=message, user_message=message), 503
    
    def put(self, self_registered=True):
        try:
            self_register = str2bool(self_registered)
        except Exception as e:
            message = f'Hubo un error durante la actualización del candidato {e}'
            return get_response_body(code=503, message=message, user_message=message), 503
