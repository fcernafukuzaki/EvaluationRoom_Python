from flask import request
from flask_restful import Resource
from common.util import get_response_body
from common.validate_handler import authorize_user
from .candidate_service import CandidateService


candidate_service = CandidateService()


class CandidateController(Resource):
    
    @authorize_user
    def get(self, uid=None, numerodocumentoidentidad=None):
        """ Obtener datos del candidato a partir del identificador del candidato o del número de documento de identidad.
        """
        response_body = None
        try:
            if uid:
                result, code, message = candidate_service.get_by_uid(uid)
            if numerodocumentoidentidad:
                result, code, message = candidate_service.get_by_document(numerodocumentoidentidad)
            response_body = {'candidato':result} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al consultar los datos del candidato {e}'
        finally:
            user_message = message
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), 404

    
    # def get(self, uid=None, email=None):
    #     try:
    #         token = request.headers['Authorization']
    #         validated = authorizer_service.validate_token(token)
    #         if validated:
    #             if uid:
    #                 result, code, message = candidate_service.get_candidate_by_uid(uid)
    #                 user_message = message
    #             if email:
    #                 correoelectronico = str(email).lower()
    #                 result, code, message = candidate_service.get_candidate_by_email(correoelectronico)
    #                 user_message = message
    #             if result:
    #                 response_body = {'candidato':result} if result else None
    #                 return get_response_body(code=200, message='OK', user_message=user_message, body=response_body), 200
    #             return get_response_body(code=code, message=message, user_message=user_message), code
    #         message = 'Operación inválida.'
    #         user_message = 'Operación inválida.'
    #         return get_response_body(code=403, message=message, user_message=user_message), 403
    #     except Exception as e:
    #         message = f'Hubo un error al obtener datos del candidato {e}'
    #         return get_response_body(code=503, message=message, user_message=message), 503
    
    def post(self, self_registered="true"):
        """ Guardar datos de un candidato.
        """
        response_body = None
        try:
            input_json = request.json
            
            nombre, apellidopaterno, apellidomaterno, correoelectronico, iddocumentoidentidad, numerodocumentoidentidad, idestadocivil, idsexo, cantidadhijos, fechanacimiento, telefonos, direcciones, tests = self.__json_candidate(input_json)

            result, code, message = candidate_service.create(nombre, apellidopaterno, apellidomaterno, 
                                                             correoelectronico, iddocumentoidentidad, numerodocumentoidentidad, 
                                                             idestadocivil, idsexo, cantidadhijos, fechanacimiento, 
                                                             self_registered, telefonos, direcciones, tests)
            
            idcandidato = result

            response_body = {'candidato':{"idCandidato":idcandidato,"correoElectronico":correoelectronico}} if idcandidato else None
        except Exception as e:
            code, message = 503, f'Hubo un error al guardar los datos del candidato {e}'
        finally:
            user_message = message
            if response_body:
                return get_response_body(code=201, message='OK', user_message=message, body=response_body), 201
            return get_response_body(code=code, message=message, user_message=user_message), 404


    def put(self, uid):
        """ Actualizar datos de un candidato.
        """
        response_body = None
        try:
            input_json = request.json
            
            nombre, apellidopaterno, apellidomaterno, correoelectronico, iddocumentoidentidad, numerodocumentoidentidad, idestadocivil, idsexo, cantidadhijos, fechanacimiento, telefonos, direcciones, tests = self.__json_candidate(input_json)

            result, code, message = candidate_service.update(uid, nombre, apellidopaterno, apellidomaterno, 
                                                             correoelectronico, iddocumentoidentidad, numerodocumentoidentidad, 
                                                             idestadocivil, idsexo, cantidadhijos, fechanacimiento, 
                                                             telefonos, direcciones, tests)
            response_body = {'candidato':result} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al actualizar los datos del candidato {e}'
        finally:
            user_message = message
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), 404

    
    @authorize_user
    def delete(self, uid):
        """ Eliminar datos de un candidato.
        """
        response_body = None
        try:
            result, code, message = candidate_service.delete(uid)
            response_body = {'candidato':result} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al eliminar los datos del candidato {e}'
        finally:
            user_message = message
            if response_body:
                return get_response_body(code=204, message='OK', user_message=message, body=response_body), 204
            return get_response_body(code=code, message=message, user_message=user_message), 404


    def __json_candidate(self, input_json):
        nombre, apellidopaterno, apellidomaterno = input_json.get('nombre'), input_json.get('apellidoPaterno'), input_json.get('apellidoMaterno')
        correoelectronico = str(input_json.get('correoElectronico', '')).lower()
        iddocumentoidentidad = input_json.get('documentoIdentidad')['idDocumentoIdentidad'] if input_json.get('documentoIdentidad') is not None else 1
        numerodocumentoidentidad = input_json.get('numeroDocumentoIdentidad')
        idestadocivil = input_json.get('estadoCivil')['idEstadoCivil'] if input_json.get('estadoCivil') is not None else 1
        idsexo = input_json.get('sexo')['idSexo'] if input_json.get('sexo') is not None else 1
        cantidadhijos = input_json.get('cantidadHijos', 0)
        fechanacimiento = input_json.get('fechaNacimiento')
        
        telefonos = [
            {
                'idtelefono': row.get("idTelefono"),
                'numero': row.get("numero")
            }
            for row in input_json.get('telefonos')
            if row.get('idTelefono') is not None
        ]

        direcciones = [
            {
                'idtipodireccion': row.get("idTipoDireccion"),
                'idpais': row.get("pais")["idPais"] if row.get("pais") is not None else None,
                'iddepartamento': row.get("departamento")["idDepartamento"] if row.get("departamento") is not None else None,
                'idprovincia': row.get("provincia")["idProvincia"] if row.get("provincia") is not None else None,
                'iddistrito': row.get("distrito")["idDistrito"] if row.get("distrito") is not None else None,
                'direccion': row.get("direccion")
            }
            for row in input_json.get('direcciones')
            if row.get('idTipoDireccion') is not None
        ]

        tests = [
            {
                'idtestpsicologico': row.get("idTestPsicologico")
            }
            for row in input_json.get('testPsicologicos')
            if row.get('idTestPsicologico') is not None
        ]
        return nombre, apellidopaterno, apellidomaterno, correoelectronico, iddocumentoidentidad, numerodocumentoidentidad, idestadocivil, idsexo, cantidadhijos, fechanacimiento, telefonos, direcciones, tests
    
    # def post(self, self_registered="true"):
    #     try:
    #         self_register = str2bool(self_registered)
    #         input_json = request.json
    #         idcandidato = input_json['idCandidato'] if field_in_dict(input_json, 'idCandidato') else None
    #         idcandidato = idcandidato if isinstance(idcandidato, int) else None
    #         nombre = input_json['nombre'] if field_in_dict(input_json, 'nombre') else None
    #         apellidopaterno = input_json['apellidoPaterno'] if field_in_dict(input_json, 'apellidoPaterno') else None
    #         apellidomaterno = input_json['apellidoMaterno'] if field_in_dict(input_json, 'apellidoMaterno') else None
    #         correoelectronico = str(input_json['correoElectronico']).lower() if field_in_dict(input_json, 'correoElectronico') else None
    #         iddocumentoidentidad = input_json['documentoIdentidad']['idDocumentoIdentidad'] if input_json['documentoIdentidad']['idDocumentoIdentidad'] > 0 else 1
    #         numerodocumentoidentidad = input_json['numeroDocumentoIdentidad'] if field_in_dict(input_json, 'numeroDocumentoIdentidad') else None
    #         idestadocivil = input_json['estadoCivil']['idEstadoCivil'] if input_json['estadoCivil']['idEstadoCivil'] > 0 else 1
    #         idsexo = input_json['sexo']['idSexo'] if input_json['sexo']['idSexo'] > 0 else 1
    #         cantidadhijos = input_json['cantidadHijos'] if field_in_dict(input_json, 'cantidadHijos') else None
    #         fechanacimiento = input_json['fechaNacimiento'] if field_in_dict(input_json, 'fechaNacimiento') else None
    #         telefonos = input_json['telefonos'] if field_in_dict(input_json, 'telefonos') else None
    #         direcciones = input_json['direcciones'] if field_in_dict(input_json, 'direcciones') else None
    #         tests = input_json['testPsicologicos'] if field_in_dict(input_json, 'testPsicologicos') else None
            
    #         if not idcandidato:
    #             _, code, _ = candidate_service.get_candidate_by_email(correoelectronico)
    #             if code == 200:
    #                 message = f'Error relacionado a Correo electrónico.'
    #                 user_message = f'Ya existe un candidato con el mismo correo electrónico. Debe ingresar un email distinto.'
    #                 return get_response_body(code=409, message=message, user_message=user_message), 409
                
    #             if numerodocumentoidentidad:
    #                 _, code, _ = candidate_service.get_candidate_by_document(numerodocumentoidentidad)
    #                 if code == 200:
    #                     message = f'Error relacionado a Número de documento.'
    #                     user_message = f'Ya existe un candidato con el mismo número de documento de identidad. Debe ingresar uno distinto.'
    #                     return get_response_body(code=409, message=message, user_message=user_message), 409

    #             result, code, message = candidate_service.add_candidate(idcandidato, nombre, apellidopaterno, apellidomaterno, iddocumentoidentidad, numerodocumentoidentidad, idestadocivil,
    #                         cantidadhijos, fechanacimiento, correoelectronico, idsexo, self_register, telefonos, direcciones)
    #             idcandidato = result
    #             user_message = message
    #             if idcandidato and tests:
    #                 result, code, message = candidate_service.add_candidate_tests(idcandidato, tests)
    #                 user_message = f"{user_message} {message}"
    #         else:
    #             result, code, message = candidate_service.update_candidate(idcandidato, nombre, apellidopaterno, apellidomaterno, iddocumentoidentidad, numerodocumentoidentidad, idestadocivil,
    #                         cantidadhijos, fechanacimiento, correoelectronico, idsexo, self_register, telefonos, direcciones)
                
    #             user_message = message
    #             if idcandidato and not tests:
    #                 result, code, message = candidate_service.get_candidate_by_uid(idcandidato)
    #                 tests_eliminar = [t["idtestpsicologico"] for t in result["psychologicaltests"]]
    #                 result, code, message = candidate_service.delete_candidate_tests_by_tests(idcandidato, tests_eliminar)
    #                 user_message = f"{user_message} {message}"
    #             if idcandidato and tests:
    #                 result, code, message = candidate_service.get_candidate_by_uid(idcandidato)
    #                 idtestpsicologico_original = [t["idtestpsicologico"] for t in result["psychologicaltests"]]
    #                 tests_nuevo = [t for t in tests if t not in idtestpsicologico_original]
    #                 tests_eliminar = [t for t in idtestpsicologico_original if t not in tests]
                    
    #                 result, code, message = candidate_service.delete_candidate_tests_by_tests(idcandidato, tests_eliminar)
    #                 user_message = f"{user_message} {message}"
                    
    #                 result, code, message = candidate_service.add_candidate_tests(idcandidato, tests_nuevo)
    #                 user_message = f"{user_message} {message}"

    #         response_body = {'candidato':{"idCandidato":idcandidato,"correoElectronico":correoelectronico}} if idcandidato else None
    #         return get_response_body(code=200, message='OK', user_message=user_message, body=response_body), 200
    #     except Exception as e:
    #         message = f'Hubo un error durante el registro del candidato {e}'
    #         return get_response_body(code=503, message=message, user_message=message), 503
