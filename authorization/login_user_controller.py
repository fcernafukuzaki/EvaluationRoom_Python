from flask import request
from flask_restful import Resource
from common.util import get_response_body
from .authorizer_service import AuthorizerService
from .login_user_service import LoginUserService

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

            response_body = {'usuario':user_object} if flag else None
        except Exception as e:
            code, message = 503, f'Hubo un error durante la consulta del usuario {e}'
        finally:
            if response_body:
                return get_response_body(code=code, message=message, user_message=user_message, body=response_body), code
            return get_response_body(code=code, message=message, user_message=message), code
