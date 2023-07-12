from flask import request
from configs.logging import logger
from common.util import get_response_body
from authorization.authorizer_service import AuthorizerService

authorizer_service = AuthorizerService()

def authorize_user(func):
    def wrapper(*args, **kwargs):
        input_header = request.headers
        token = input_header.get('Authorization')
        correoelectronico = input_header.get('correoElectronico')

        flag, respuesta, codigo, _ = authorizer_service.validate_recruiter_identify(token, correoelectronico)
        logger.debug("Response from validate recruiter.", respuesta=respuesta, codigo=codigo)

        if flag:
            return func(*args, **kwargs)
        else:
            code, message = 403, 'Operación inválida.'
            user_message = message
            return get_response_body(code=code, message=message, user_message=user_message), code
    return wrapper
