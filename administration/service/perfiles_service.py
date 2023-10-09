from configs.logging import logger
from administration.repository.perfiles_repository import PerfilesRepository


perfiles_repository = PerfilesRepository()


class PerfilesService():
    """
    Acceso a los datos de los perfiles.
    """

    def get_perfiles(self):
        """
        Descripción:
            Retornar datos de los perfiles de acceso al sistema.
        Input:
            - None.
        
        Output:
            - result:object Lista de perfiles.
            - code:int Código de respuesta. [200:OK, 404:Not Found, 503:Error]
            - message:str Mensaje de salida.
        """
        result = None
        try:
            flag, message, result = perfiles_repository.get_all()
            code = 200 if flag else 404
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de perfiles en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message
    

    def get_perfil(self, uid):
        """
        Descripción:
            Retornar datos de un perfil.
        Input:
            - uid:int Identificador del perfil.
        
        Output:
            - result:object Datos del perfil.
            - code:int Código de respuesta. [200:OK, 404:Not Found, 503:Error]
            - message:str Mensaje de salida.
        """
        result = None
        try:
            flag, message, result = perfiles_repository.get(uid=uid)
            code = 200 if flag else 404
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de perfil {uid} en base de datos {e}'
        finally:
            logger.info("Response from perfil.", uid=uid, message=message)
            return result, code, message
    

    def add_perfil(self, nombre:str):
        """
        Descripción:
            Agregar un nuevo perfil.
        Input:
            - nombre:str Nombre del perfil.
        
        Output:
            - result:int Identificador del perfil.
            - code:int Código de respuesta. [200:OK, 404:Not Found, 503:Error]
            - message:str Mensaje de salida.
        """
        result = None
        try:
            flag, message, result = perfiles_repository.add(nombre=nombre)
            code = 200 if flag else 404
        except Exception as e:
            code, message = 503, f'Hubo un error al registrar perfil en base de datos {e}'
        finally:
            logger.debug("Perfil inserted.", message=message)
            return result, code, message
    

    def update_perfil(self, uid:int, nombre:str):
        """
        Descripción:
            Actualizar datos de un perfil.
        Input:
            - uid:int Identificador del perfil.
            - nombre:str Nombre del perfil.
        
        Output:
            - result:int Identificador del perfil.
            - code:int Código de respuesta. [200:OK, 404:Not Found, 503:Error]
            - message:str Mensaje de salida.
        """
        result = None
        try:
            flag, message, result = perfiles_repository.update(uid=uid, nombre=nombre)
            code = 200 if flag else 404
        except Exception as e:
            code, message = 503, f'Hubo un error al actualizar perfil en base de datos {e}'
        finally:
            logger.debug("Perfil updated.", message=message)
            return result, code, message
