import json
from os import environ
from common.util import invoke_api, get_response_body
from configs.logging import logger


class APIGatewayNotificacionService():

    def notificar_error(self, email, observacion, detalle):
        response_body = None
        try:
            URL = environ.get("API_SNS")
            encoded_body = json.dumps({
                "correoElectronico": email,
                "observacion": observacion,
                "detalle": detalle
            })
            HEADERS = {'Content-Type': 'application/json', 'Authorization': email}
            response = invoke_api(url=URL, 
                                  body=encoded_body, 
                                  headers=HEADERS,
                                  method='POST',
                                  retries=False)
            status = response.status
            logger.debug('Resultado de API: {} {}'.format(status, response.data))
            
            if status == 200:
                user_message = 'Se envió notificación del candidato con el correo electronico {} a soporte técnico'.format(email)
                logger.info(user_message)
                flag, message  = True, user_message
                response_body = json.loads(response.data.decode('utf-8'))
            else:
                user_message = 'No se envió notificación del candidato con el correo electronico {}'.format(email)
                logger.info(user_message)
                flag, message  = False, user_message
        except Exception as e:
            user_message = f'Error durante consumo de servicio de envío de notificación. {e}'
            logger.info(user_message)
            flag, status, message = False, 503, 'Ocurrió un error.'
        finally:
            return flag, get_response_body(code=status, 
                                           message=message, 
                                           user_message=user_message, 
                                           body=response_body)
