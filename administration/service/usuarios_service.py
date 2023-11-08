from configs.logging import logger
from administration.repository.usuarios_repository import UsuariosRepository
from administration.repository.perfiles_repository import PerfilesRepository


usuarios_repository = UsuariosRepository()
perfiles_repository = PerfilesRepository()


class UsuariosService():
    """
    Acceso a los datos de los usuarios o de un usuario.
    """

    def get_usuarios(self):
        """
        Descripción:
            Retornar datos de los usuarios que tienen acceso al sistema.
        Input:
            - None.
        
        Output:
            - result:object Lista de usuarios.
            - code:int Código de respuesta. [200:OK, 404:Not Found, 503:Error]
            - message:str Mensaje de salida.
        """
        result = None
        try:
            flag, message, result = usuarios_repository.get_all()
            code = 200 if flag else 404
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de usuarios en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message
    

    def get_usuario(self, uid:int):
        """
        Descripción:
            Retornar datos de un usuario.
        Input:
            - uid:int Identificador del usuario.
        
        Output:
            - result:object Datos del usuario.
            - code:int Código de respuesta. [200:OK, 404:Not Found, 503:Error]
            - message:str Mensaje de salida.
        """
        result = None
        try:
            flag, message, result = usuarios_repository.get(uid=uid)
            code = 200 if flag else 404
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de usuario {uid} en base de datos {e}'
        finally:
            logger.info("Response from usuario.", uid=uid, message=message)
            return result, code, message
    

    def add_usuario(self, nombre:str, email:str, activo:bool, idempresa:int):
        """
        Descripción:
            Agregar un nuevo usuario.
        Input:
            - nombre:str Nombre del usuario.
            - email:str Correo electrónico del usuario.
            - activo:bool [True, False] Activo o no activo.
            - idempresa: int. Identificador de la empresa.
        
        Output:
            - result:int Identificador del usuario.
            - code:int Código de respuesta. [200:OK, 404:Not Found, 503:Error]
            - message:str Mensaje de salida.
        """
        result = None
        try:
            flag, message, result = usuarios_repository.add(nombre=nombre, 
                                                            email=email, 
                                                            activo=activo, 
                                                            idempresa=idempresa)
            code = 200 if flag else 404
        except Exception as e:
            code, message = 503, f'Hubo un error al registrar usuario en base de datos {e}'
        finally:
            logger.debug("Usuario inserted.", message=message)
            return result, code, message
    

    def update_usuario(self, uid:int, nombre:str, email:str, activo:bool, idempresa:int, perfiles=None):
        """
        Descripción:
            Actualizar datos de un usuario.
        Input:
            - uid:int Identificador del usuario.
            - nombre:str Nombre del usuario.
            - email:str Correo electrónico del usuario.
            - activo:bool [True, False] Activo o no activo.
            - idempresa: int. Identificador de la empresa.
        
        Output:
            - result:int Identificador del usuario.
            - code:int Código de respuesta. [200:OK, 404:Not Found, 503:Error]
            - message:str Mensaje de salida.
        """
        result = None
        try:
            flag, message, result = usuarios_repository.update(uid=uid, 
                                                               nombre=nombre, 
                                                               email=email, 
                                                               activo=activo, 
                                                               idempresa=idempresa)
            
            if flag:
                flag, message, result = perfiles_repository.assign_to(uid=uid, perfiles=perfiles)
            
            logger.debug("Usuario updated.", id_usuario=uid)
            result, code, message = uid, 200, 'Se actualizó usuario en base de datos.'
        except Exception as e:
            code, message = 503, f'Hubo un error al actualizar usuario en base de datos {e}'
        finally:
            logger.debug("Usuario updated.", message=message)
            return result, code, message
