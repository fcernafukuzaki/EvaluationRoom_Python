from flask import request
from flask_restful import Resource
from common.util import get_response_body
from common.validate_handler import authorize_user
from .selectionprocess_service import SelectionProcessService


selectionprocess_service = SelectionProcessService()


class Dashboard(Resource):
    
    @authorize_user
    def post(self, email=None):
        """ Obtener los datos de los procesos de selección.
        """
        response_body = None
        try:
            result, code, message = selectionprocess_service.get_candidates_without_selectionprocess(email)
            response_body = {'selectionprocess':result} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al consultar los procesos de selección {e}'
        finally:
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=message), 404
