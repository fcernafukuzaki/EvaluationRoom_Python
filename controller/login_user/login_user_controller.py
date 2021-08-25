from flask import request
from flask_restful import Resource
from common.util import field_in_dict, get_response_body
from service.authorizer_service import AuthorizerService
from objects.login_user import LoginUser
from service.login_user_service import LoginUserService

authorizer_service = AuthorizerService()
login_user_service = LoginUserService()

class LoginUserController(Resource):
    
    def post(self):
        try:
            input_json = request.json
            input_header = request.headers
            hash = input_header['Authorization'] if field_in_dict(input_header, 'Authorization') else None
            correoelectronico = input_json['correoelectronico'] if field_in_dict(input_json, 'correoelectronico') else None
            flag, message, code, user_object = authorizer_service.validate_recruiter_active(hash, correoelectronico)
            user_message = message

            idusuario = user_object['idusuario'] if flag else 0
            email = None if flag else correoelectronico
            result, _, message_aux = login_user_service.add_login_user(idusuario, hash, email)
            user_message = f"{user_message} {message_aux}"

            response_body = {'usuario':{"idusuario":idusuario,"correoelectronico":correoelectronico,"perfiles":user_object['perfiles']}} if flag else None
            return get_response_body(code=code, message=message, user_message=user_message, body=response_body), code
        except Exception as e:
            message = f'Hubo un error durante la consulta del usuario {e}'
            return get_response_body(code=503, message=message, user_message=message), 503
