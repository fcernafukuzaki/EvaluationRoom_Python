from configs.resources import db
from configs.logging import logger
from .service.usuario_validar_service import UsuarioValidarService
from authorization.service.login_user_service import LoginUserService

usuariovalidar_service = UsuarioValidarService()
loginuser_service = LoginUserService()

class AuthorizerService():

    def validate_recruiter_identify(self, token:str, email:str):
        ''' 
        Descripción:
            Validar la identidad del reclutador.
        Input:
            - token:str Hash recuperado por servicio de autenticación.
            - email:str correo electrónico.
        
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - code:int Código de respuesta. [200:OK, 404:Not Found, 503:Error]
            - result:int Identificador del usuario.
        '''
        result = None
        if email and token:
            email_valido, mensaje, usuario = usuariovalidar_service.get_data(email)
            if email_valido:
                is_valid = loginuser_service.validate_hash(token, usuario.get("idusuario"))
                if is_valid:
                    flag, message, code, result = True, 'Usuario valido.', 200, usuario.get("idusuario")
                    return flag, message, code, result
                flag, message, code, result = False, 'Operación no valida.', 403, None
                return flag, message, code, result
            flag, message, code, result = False, mensaje, 404, None
            return flag, message, code, result
        flag, message, code, result = False, 'Usuario no valido.', 404, None
        return flag, message, code, result


    def validate_recruiter_active(self, token:str, email:str):
        ''' 
        Descripción:
            Validar que el reclutador se encuentra con estado activo.
        Input:
            - token:str Hash recuperado por servicio de autenticación.
            - email:str correo electrónico.
        
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - code:int Código de respuesta. [200:OK, 404:Not Found, 503:Error]
            - result:int Identificador del usuario.
        '''
        if email and token:
            email_valido, mensaje, usuario = usuariovalidar_service.get_data(email)
            if email_valido:
                return True, 'Usuario valido.', 200, usuario
            return False, mensaje, 404, None
        return False, 'Usuario no valido.', 404, None


    def validate_candidate(self, data):
        ''' Validar que el valor no sea vacío.
        '''
        if data:
            return True, 'Operación valida.', 200, None
        return False, 'Operación no valida.', 403, None
