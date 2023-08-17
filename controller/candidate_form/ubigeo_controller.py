from flask_restful import Resource
from common.util import get_response_body
from .ubigeo_service import UbigeoService


ubigeo_service = UbigeoService()


class UbigeoController(Resource):

    def get(self, idcountry=None, iddepartamento=None, idprovincia=None):
        """ Obtener datos de ubigeo.
        """
        response_body = None
        try:
            if not idcountry:
                result, code, message = ubigeo_service.get_countries()
                response_body = {'paises':result} if result else None
                
            if idcountry and not iddepartamento:
                result, code, message = ubigeo_service.get_departamentos_by_country(idcountry)
                response_body = {'departamentos':result} if result else None
                
            if idcountry and iddepartamento and not idprovincia:
                result, code, message = ubigeo_service.get_provincias_by_ids(idcountry, iddepartamento)
                response_body = {'provincias':result} if result else None
                
            if idcountry and iddepartamento and idprovincia:
                result, code, message = ubigeo_service.get_distritos_by_ids(idcountry, iddepartamento, idprovincia)
                response_body = {'distritos':result} if result else None
        except Exception as e:
            code, message = 503, f'Hubo un error al consultar ubigeo {e}'
        finally:
            user_message = message
            if response_body:
                return get_response_body(code=200, message='OK', user_message=message, body=response_body), 200
            return get_response_body(code=code, message=message, user_message=user_message), 404
