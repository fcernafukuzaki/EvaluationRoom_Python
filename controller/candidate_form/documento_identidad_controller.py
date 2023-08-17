from flask_restful import Resource
from common.util import get_response_body
from common.validate_handler import authorize_user
from .documento_identidad_service import DocumentoIdentidadService


documento_identidad_service = DocumentoIdentidadService()


class DocumentoIdentidadController(Resource):

    @authorize_user
    def get(self):
        """ Obtener documentos de identidad.
        """
        response_body = None
        try:
            result, code, message = documento_identidad_service.get_documentos_identidad()
            response_body = {'documentos_identidad':result} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al consultar documentos de identidad {e}'
            user_message = message
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), 404
