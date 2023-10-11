from configs.logging import logger
from authorization.repository.login_user_repository import LoginUserRepository


loginuser_repository = LoginUserRepository()


class LoginUserService():
    """
    Monitorear actividad de acceso al sistema.
    """

    def add_login_user(self, id_user:int, hash:str, email:str):
        """
        Descripción:
            Registrar intento de acceso al sistema.
        Input:
            - id_user:int Identificador de usuario.
            - hash:str hash recuperado por servicio de autenticación.
            - email:str correo electrónico.
        
        Output:
            - result:object Login_user.
            - code:int Código de respuesta. [200:OK, 404:Not Found, 503:Error]
            - message:str Mensaje de salida.
        """
        result = None
        try:
            flag, message, result = loginuser_repository.add(id_user, hash, email)
            code = 200 if flag else 404
        except Exception as e:
            code, message = 503, f'Hubo un error al registrar login en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message


    def validate_hash(self, hash:str, uid:int):
        """
        Descripción:
            Validar que un hash no está volviendo a ser utilizado.
        Input:
            - hash:str hash recuperado por servicio de autenticación.
            - uid:int Identificador de usuario.
        
        Output:
            - flag:bool (True, False)
        """
        response = loginuser_repository.is_valid_hash(hash, uid)
        if response:
            return True
        return False
