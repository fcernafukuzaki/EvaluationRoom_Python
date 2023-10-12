import os
import io
from flask import send_file
from configs.logging import logger
from common.util import invoke_api
from authorization.authorizer_service import AuthorizerService

authorizer_service = AuthorizerService()

class PsychologicalTestInterpretacionService():
    
    def create(self, idcandidato:int):
        """
        Descripción:
            Interpretar los resultados de las pruebas psicológicas.
        Input:
            - idcandidato:int Identificador del candidato/paciente.
        
        Output:
            - result:object Mensaje.
            - code:int Código de respuesta. [200:OK, 404:Not Found, 503:Error]
            - message:str Mensaje de salida.
        """
        result = None
        try:
            api = os.environ['API']
            url = f'{api}/testpsicologico/interpretacion/candidato/{idcandidato}'
            logger.debug("", url=url)
            response = invoke_api(url, body=None, method='GET')
            logger.debug('Resultado de API:', status=response.status, data=response.data)
            response_body = "OK"
            result, code, message = response_body, 200, 'OK'
        except Exception as e:
            logger.error("Error service.", uid=idcandidato, error=e)
            code, message = 503, f'Hubo un error al generar la interpretación {e}'
        finally:
            logger.info("Response from generate interpretation.", uid=idcandidato, message=message)
            return result, code, message


    def download(self, uid:int, email:str, token:str):
        """
        Descripción:
            Descargar el informe psicológico.
        Input:
            - idcandidato:int Identificador del candidato/paciente.
        
        Output:
            - result:object Archivo.
        """
        result = None
        try:
            api = os.environ['API']
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
            logger.error("Error service.", uid=uid, error=e)
            return None
