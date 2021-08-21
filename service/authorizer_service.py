import json
from common.util import invoke_api


class AuthorizerService():

    def validate_recruiter_identify(self, token, email):
        if email and token:
            url = 'https://api.evaluationroom.com/reclutador_identificador_validar/'
            data = {"Authorization": token, "correoelectronico": email}
            encoded_data = json.dumps(data).encode('utf-8')
            response = invoke_api(url, encoded_data, 'POST')
            print('Resultado de API: {} {}'.format(response.status, response.data))
            if response.status == 200:
                return True, 'Usuario valido', response.status, json.loads(response.data.decode('utf-8'))['idusuario']
            return False, json.loads(response.data.decode('utf-8'))['mensaje'], response.status, None
        return False, 'Usuario no valido.', 404, None
    
    def validate_recruiter_active(self, token, email):
        if email and token:
            url = 'https://api.evaluationroom.com/reclutador_identificador_validar/reclutador_email_validar'
            data = {"Authorization": token, "correoelectronico": email}
            encoded_data = json.dumps(data).encode('utf-8')
            response = invoke_api(url, encoded_data, 'POST')
            print('Resultado de API: {} {}'.format(response.status, response.data))
            if response.status == 200:
                return True, 'Usuario valido', response.status, json.loads(response.data.decode('utf-8'))
            return False, json.loads(response.data.decode('utf-8'))['mensaje'], response.status, None
        return False, 'Usuario no valido.', 404, None
    
    def validate_token(self, token):
        if token:
            return True
        return False
