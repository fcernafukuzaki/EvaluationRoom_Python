from flask import request
from flask_restful import Resource
from common.util import get_response_body
from service.authorizer_service import AuthorizerService
from service.login_user_service import LoginUserService

authorizer_service = AuthorizerService()
login_user_service = LoginUserService()

class LoginUserController(Resource):
    
    def post(self):
        try:
            input_json = request.json
            input_header = request.headers
            token = input_header.get('Authorization')
            correoelectronico = input_json.get('correoelectronico')
            flag, message, code, user_object = authorizer_service.validate_recruiter_active(token, correoelectronico)
            user_message = message
            idusuario = user_object['idusuario'] if flag else 0
            result, _, message_aux = login_user_service.add_login_user(idusuario, token, correoelectronico)
            user_message = f"{user_message} {message_aux}"

            response_body = {'usuario':{"idusuario":idusuario,"correoelectronico":correoelectronico,"perfiles":user_object['perfiles']}} if flag else None
            return get_response_body(code=code, message=message, user_message=user_message, body=response_body), code
        except Exception as e:
            message = f'Hubo un error durante la consulta del usuario {e}'
            return get_response_body(code=503, message=message, user_message=message), 503
