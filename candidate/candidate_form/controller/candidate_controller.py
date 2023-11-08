from flask_restful import Resource
from common.util import get_response_body
from common.validate_handler import authorize_user
from candidate.candidate_form.service.candidate_service import CandidateService


candidate_service = CandidateService()


class CandidateController(Resource):

    @authorize_user
    def get(self, uid=None):
        """Obtener datos del candidato a partir del identificador del candidato."""
        response_body = None
        try:
            if uid:
                result, code, message = candidate_service.get_by_uid(uid)
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

    @authorize_user
    def delete(self, uid):
        """Eliminar datos de un candidato."""
        response_body = None
        try:
            result, code, message = candidate_service.delete(uid)
            response_body = {"candidato": result} if result else None
        except Exception as e:
            code, message = (
                503,
                f"Hubo un error al eliminar los datos del candidato {e}",
            )
        finally:
            user_message = message
            if response_body:
                return (
                    get_response_body(
                        code=204, message="OK", user_message=message, body=response_body
                    ),
                    204,
                )
            return (
                get_response_body(
                    code=code, message=message, user_message=user_message
                ),
                404,
            )
