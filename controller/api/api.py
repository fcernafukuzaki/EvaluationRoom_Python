from flask import request
from flask_restful import Resource
from common.util import field_in_dict, get_response_body
import json
import os
from common.util import invoke_api


class PsychologicalTestInterpretacionController(Resource):
    
    def get(self, idcandidato):
        try:
            if idcandidato:
                api = os.environ['API']
                url = f'{api}/testpsicologico/interpretacion/candidato/{idcandidato}'
                response = invoke_api(url, None, 'GET')
                print('Resultado de API: {} {}'.format(response.status, response.data))
                response_body = {'mensaje':"OK"}
                return get_response_body(code=200, message="OK", user_message="OK", body=response_body), 200
        except Exception as e:
            message = f'Hubo un error durante la consulta del usuario {e}'
            return get_response_body(code=503, message=message, user_message=message), 503
