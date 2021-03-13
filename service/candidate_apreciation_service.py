import urllib3
import json


class CandidateApreciationService():

    def assign_candidateapreciation_to_selectionprocess(self, token, email, idcandidato, idclient, idjobposition):
        flag, message, code, candidateapreciation = self._get_candidateapreciation(token, email, idcandidato)
        
        if len(candidateapreciation) > 0:
            flag, message, code = self._add_candidateapreciation(token, email, idcandidato, idclient, idjobposition, candidateapreciation[0]['idreclutador'], candidateapreciation[0]['apreciacion'])
            if flag:
                print('Apreciation added.')
            else:
                print('Error adding apreciation.')

    def _get_candidateapreciation(self, token, email, idcandidato):
        if email and token:
            http = urllib3.PoolManager()
            url = 'https://api.evaluationroom.com/examen/candidato/entrevista/apreciacion/obtener'

            data = {"headers": {"Authorization": token, "correoelectronico": email}, "idcandidato": idcandidato}
            encoded_data = json.dumps(data).encode('utf-8')

            response = http.request('POST',
                                    url,
                                    body=encoded_data,
                                    headers={'Content-Type': 'application/json'})
            print('Resultado de API: {} {}'.format(response.status, response.data))
            if response.status == 200:
                if json.loads(response.data.decode('utf-8'))['statusCode'] == 200:
                    return True, 'Usuario valido', response.status, json.loads(response.data.decode('utf-8'))['body']
            return False, json.loads(response.data.decode('utf-8'))['mensaje'], response.status, None
        return False, 'Usuario no valido.', 404, None
    
    def _add_candidateapreciation(self, token, email, idcandidato, idclient, idjobposition, idrecruiter, apreciation):
        if email and token:
            http = urllib3.PoolManager()
            url = 'https://api.evaluationroom.com/examen/candidato/entrevista/apreciacion/guardar'

            data = {
                "headers": {
                    "Authorization": token,
                    "correoelectronico": email
                },
                "idcandidato": idcandidato, 
                "idcliente_idpuestolaboral": "{}.{}".format(idclient, idjobposition), 
                "idcliente": idclient,
                "idpuestolaboral": idjobposition, 
                "idreclutador": idrecruiter, 
                "apreciacion": apreciation
            }
            encoded_data = json.dumps(data).encode('utf-8')

            response = http.request('POST',
                                    url,
                                    body=encoded_data,
                                    headers={'Content-Type': 'application/json'})
            print('Resultado de API: {} {}'.format(response.status, response.data))
            if response.status == 200:
                if json.loads(response.data.decode('utf-8'))['statusCode'] == 200:
                    return True, 'Usuario valido', response.status
            return False, json.loads(response.data.decode('utf-8'))['mensaje'], response.status
        return False, 'Usuario no valido.', 404

