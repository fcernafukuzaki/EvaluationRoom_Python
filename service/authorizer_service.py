import urllib3
import json


class AuthorizerService():

    def validate_recruiter_identify(self, token, email):
        if email and token:
            http = urllib3.PoolManager()
            url = 'https://api.evaluationroom.com/reclutador_identificador_validar/'

            data = {"Authorization": token, "correoelectronico": email}
            encoded_data = json.dumps(data).encode('utf-8')

            response = http.request('POST',
                                    url,
                                    body=encoded_data,
                                    headers={'Content-Type': 'application/json'})
            print('Resultado de API: {} {}'.format(response.status, response.data))
            if response.status == 200:
                return True, 'Usuario valido', response.status
            return False, json.loads(response.data.decode('utf-8'))['mensaje'], response.status
        return False, 'Usuario no valido.', 404
