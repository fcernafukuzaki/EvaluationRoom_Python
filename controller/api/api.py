from flask import request, send_file
from flask_restful import Resource
from common.util import field_in_dict, get_response_body
import json
import os
import io
from common.util import invoke_api
from service.authorizer_service import AuthorizerService

authorizer_service = AuthorizerService()

class PsychologicalTestInterpretacionController(Resource):
    
    def get(self, idcandidato=None, uid=None, email=None):
        try:
            api = os.environ['API']
            print("PsychologicalTestInterpretacionController:{}|{}|{}|{}".format(idcandidato,uid,email,api))
            if idcandidato:
                url = f'{api}/testpsicologico/interpretacion/candidato/{idcandidato}'
                print(url)
                response = invoke_api(url, body=None, method='GET')
                print('Resultado de API: {} {}'.format(response.status, response.data))
                response_body = {'mensaje':"OK"}
                return get_response_body(code=200, message="OK", user_message="OK", body=response_body), 200
            if uid:
                print(request.headers)
                print(request.json)
                token = request.headers['Authorization']
                print(f"{token}")
                flag, respuesta, codigo, _ = authorizer_service.validate_recruiter_identify(token, email)
                print("{}|{}".format(flag,respuesta))
                if flag:
                    url = f'{api}/testpsicologico/download/informe/{uid}'
                    print(url)
                    response = invoke_api(url, body=None, method='GET')
                    print('Resultado de API de descarga: {} | {}'.format(response.status, response.headers.get('content-disposition')))
                    filename = str(response.headers.get('content-disposition')).split("filename=")
                    filename = filename[1][1:-1].strip()
                    mimetype = response.headers.get('content-type')
                    return send_file(io.BytesIO(response.data),mimetype=mimetype,as_attachment=True,attachment_filename=filename)
        except Exception as e:
            message = f'Hubo un error durante la consulta del usuario {e}'
            return get_response_body(code=503, message=message, user_message=message), 503
