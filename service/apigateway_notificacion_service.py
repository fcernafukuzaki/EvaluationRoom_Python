import json
import ast
import urllib3

class APIGatewayNotificacionService():

    def notificar_error(self, email, observacion, detalle):
        try:
            http = urllib3.PoolManager()
            url = 'https://api.evaluationroom.com/v1/candidateerrorexam/notify/technicalsupport'
            encoded_body = json.dumps({
                "correoElectronico": email,
                "observacion": observacion,
                "detalle": detalle
            })
            response = http.request('POST',
                                    url,
                                    headers={'Content-Type': 'application/json', 'Authorization': email},
                                    body=encoded_body,
                                    retries=False)
            print('Resultado de API: {} {}'.format(response.status, response.data))
            if response.status == 200:
                print('Se envió notificación del candidato con el correo electronico {} a soporte técnico'.format(email))
                return True, json.loads(response.data.decode('utf-8'))
            print('No se envió notificación del candidato con el correo electronico {}'.format(email))
            return False, None
        except:
            print('Error durante consumo de servicio de envío de notificación.')
            return False, None