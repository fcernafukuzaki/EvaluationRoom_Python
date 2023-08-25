from flask import request
from flask_restful import Resource
from common.util import get_response_body
from .candidate_service import CandidateService


candidate_service = CandidateService()


class CandidateFormController(Resource):
    def get(self, email=None, numerodocumentoidentidad=None):
        """Obtener datos del candidato a partir del correo electrónico o el número de documento de identidad."""
        response_body = None
        try:
            if numerodocumentoidentidad:
                result, code, message = candidate_service.get_by_document(
                    numerodocumentoidentidad
                )
            if email:
                correoelectronico = str(email).lower()
                result, code, message = candidate_service.get_by_email(
                    correoelectronico
                )
            response_body = {"candidato": result} if result else None
        except Exception as e:
            code, message = (
                503,
                f"Hubo un error al consultar los datos del candidato {e}",
            )
        finally:
            user_message = message
            if response_body:
                return (
                    get_response_body(
                        code=200, message="OK", user_message=message, body=response_body
                    ),
                    200,
                )
            return (
                get_response_body(
                    code=code, message=message, user_message=user_message
                ),
                404,
            )

    def post(self, self_registered="true"):
        """Guardar datos de un candidato."""
        response_body = None
        try:
            input_json = request.json

            (
                nombre,
                apellidopaterno,
                apellidomaterno,
                correoelectronico,
                iddocumentoidentidad,
                numerodocumentoidentidad,
                idestadocivil,
                idsexo,
                cantidadhijos,
                fechanacimiento,
                telefonos,
                direcciones,
                tests,
            ) = candidate_service.json_candidate(input_json)

            # user_message = f'Ya existe un candidato con el mismo correo electrónico. Debe ingresar un email distinto.'
            # user_message = f'Ya existe un candidato con el mismo número de documento de identidad. Debe ingresar uno distinto.'

            result, code, message = candidate_service.create(
                nombre,
                apellidopaterno,
                apellidomaterno,
                correoelectronico,
                iddocumentoidentidad,
                numerodocumentoidentidad,
                idestadocivil,
                idsexo,
                cantidadhijos,
                fechanacimiento,
                self_registered,
                telefonos,
                direcciones,
                tests,
            )

            idcandidato = result

            response_body = (
                {
                    "candidato": {
                        "idCandidato": idcandidato,
                        "correoElectronico": correoelectronico,
                    }
                }
                if idcandidato
                else None
            )
        except Exception as e:
            code, message = 503, f"Hubo un error al guardar los datos del candidato {e}"
        finally:
            user_message = message
            if response_body:
                return (
                    get_response_body(
                        code=201, message="OK", user_message=message, body=response_body
                    ),
                    201,
                )
            return (
                get_response_body(
                    code=code, message=message, user_message=user_message
                ),
                404,
            )

    def put(self, uid):
        """Actualizar datos de un candidato."""
        response_body = None
        try:
            input_json = request.json

            (
                nombre,
                apellidopaterno,
                apellidomaterno,
                correoelectronico,
                iddocumentoidentidad,
                numerodocumentoidentidad,
                idestadocivil,
                idsexo,
                cantidadhijos,
                fechanacimiento,
                telefonos,
                direcciones,
                tests,
            ) = candidate_service.json_candidate(input_json)

            result, code, message = candidate_service.update(
                uid,
                nombre,
                apellidopaterno,
                apellidomaterno,
                correoelectronico,
                iddocumentoidentidad,
                numerodocumentoidentidad,
                idestadocivil,
                idsexo,
                cantidadhijos,
                fechanacimiento,
                telefonos,
                direcciones,
                tests,
            )
            response_body = {"candidato": result} if result else None
        except Exception as e:
            code, message = (
                503,
                f"Hubo un error al actualizar los datos del candidato {e}",
            )
        finally:
            user_message = message
            if response_body:
                return (
                    get_response_body(
                        code=200, message="OK", user_message=message, body=response_body
                    ),
                    200,
                )
            return (
                get_response_body(
                    code=code, message=message, user_message=user_message
                ),
                404,
            )
