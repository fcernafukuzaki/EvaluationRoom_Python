import os
import io
from flask import send_file
from flask_restful import Resource
from configs.logging import logger
from common.util import invoke_api, get_response_body
from authorization.authorizer_service import AuthorizerService

authorizer_service = AuthorizerService()

class PsychologicalTestInterpretacionController(Resource):
    
    def get(self, idcandidato=None, uid=None, email=None, token=None):
        try:
            api = os.environ['API']
            logger.debug("PsychologicalTestInterpretacionController", idcandidato=idcandidato, uid=uid, email=email, api=api)
            if idcandidato:
                url = f'{api}/testpsicologico/interpretacion/candidato/{idcandidato}'
                logger.debug("", url=url)
                response = invoke_api(url, body=None, method='GET')
                logger.debug('Resultado de API:', status=response.status, data=response.data)
                response_body = {'mensaje':"OK"}
                return get_response_body(code=200, message="OK", user_message="OK", body=response_body), 200
            if uid:
                flag, respuesta, codigo, _ = authorizer_service.validate_recruiter_identify(token, email)
                
                if flag:
                    url = f'{api}/testpsicologico/download/informe/{uid}'
                    logger.debug("", url=url)
                    response = invoke_api(url, body=None, method='GET')
                    logger.debug('Resultado de API de descarga:', status=response.status, content=response.headers.get('content-disposition'))
                    filename = str(response.headers.get('content-disposition')).split("filename=")
                    filename = filename[1][1:-1].strip()
                    mimetype = response.headers.get('content-type')
                    return send_file(io.BytesIO(response.data),mimetype=mimetype,as_attachment=True,download_name=filename)
        except Exception as e:
            message = f'Hubo un error durante la consulta del usuario {e}'
            return get_response_body(code=503, message=message, user_message=message), 503
