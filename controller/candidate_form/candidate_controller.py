from flask import request
from flask_restful import Resource
from common.util import field_in_dict, get_response_body
from objects.candidate import Candidate
from service.candidate_form.candidate_service import CandidateService

candidate_service = CandidateService()

class CandidateController(Resource):
    
    def post(self):
        try:
            input_json = request.json
            idcandidato = input_json['idCandidato'] if field_in_dict(input_json, 'idCandidato') else None
            nombre = input_json['nombre']
            apellidopaterno = input_json['apellidoPaterno']
            apellidomaterno = input_json['apellidoMaterno']
            correoelectronico = str(input_json['correoElectronico']).lower()
            iddocumentoidentidad = input_json['documentoIdentidad']['idDocumentoIdentidad']
            numerodocumentoidentidad = input_json['numeroDocumentoIdentidad']
            idestadocivil = input_json['estadoCivil']['idEstadoCivil']
            idsexo = input_json['sexo']['idSexo']
            cantidadhijos = input_json['cantidadHijos']
            fechanacimiento = input_json['fechaNacimiento']
            telefonos = input_json['telefonos'] if field_in_dict(input_json, 'telefonos') else None
            direcciones = input_json['direcciones'] if field_in_dict(input_json, 'direcciones') else None
            tests = input_json['testPsicologicos'] if field_in_dict(input_json, 'testPsicologicos') else None
            
            result, code, message = candidate_service.add_candidate(idcandidato, nombre, apellidopaterno, apellidomaterno, iddocumentoidentidad, numerodocumentoidentidad, idestadocivil,
                        cantidadhijos, fechanacimiento, correoelectronico, idsexo, True, telefonos, direcciones)
            idcandidato = result
            user_message = message
            if idcandidato and tests:
                result, code, message = candidate_service.add_candidate_tests(idcandidato, tests)
                user_message = f"{user_message} {message}"

            response_body = {'candidato':idcandidato} if idcandidato else None
            return get_response_body(code=200, message='OK', user_message=user_message, body=response_body), 200
        except Exception as e:
            message = f'Hubo un error durante el registro del candidato {e}'
            return get_response_body(code=503, message=message, user_message=message), 503
