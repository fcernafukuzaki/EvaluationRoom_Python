from datetime import datetime, timezone
from configs.resources import db, text
from configs.logging import logger


class LoginUserRepository():
    
    def add(self, id_user:int, hash:str, email:str):
        """ 
        Descripción:
            Registrar intento de acceso al sistema.
        Input:
            - id_user:int Identificador de usuario.
            - hash:str hash recuperado por servicio de autenticación.
            - email:str correo electrónico.
        
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result:int Identificador del usuario.
        """
        result = None
        try:
            date_login = datetime.now(timezone.utc)

            sql_query = f"INSERT INTO evaluationroom.login_user \
            (iduser, hash, date_login, email) \
            VALUES \
            ({id_user}, '{hash}', '{date_login}', '{email}') \
            "

            # Ejecutar la consulta SQL
            db.execute(text(sql_query))
            db.commit()
            
            logger.debug("User logged inserted.", email=email)
            result, flag, message = id_user, True, 'Se registró login en base de datos.'
        except Exception as e:
            logger.error("Error al registrar login.", error=e)
            db.rollback()
            flag, message = False, f'Hubo un error al registrar login en base de datos {e}'
        finally:
            logger.info(message)
            return flag, message, result


    def is_valid_hash(self, hash:str, idusuario:int):
        """
        Descripción:
            Validar que un usuario está autorizado a ingresar, 
            se encuentra activo a través del correo electrónico y su
            hash no ha sido utilizado anteriormente.
        Input:
            - hash:str hash recuperado por servicio de autenticación.
            - idusuario:int Identificador de usuario.
        
        Output:
            - result:object
        """
        result = None
        try:
            if hash:
                sql_query = f"""
                SELECT iduser, hash, date_login, email
                FROM evaluationroom.login_user
                WHERE hash='{hash}'
                AND date_logout IS NULL
                AND iduser={idusuario}
                """
                response_database = db.execute(text(sql_query))

                if int(response_database.rowcount) > 0:
                    for row in response_database:
                        result = {
                            'iduser': row.iduser,
                            'hash': row.hash,
                            'email': row.email,
                        }
                    logger.debug("User hash is valid.", uid=idusuario)
                else:
                    logger.debug("User hash is not valid.", uid=idusuario)
        except Exception as e:
            logger.error("Error al validar hash.", error=e)
            db.rollback()
        finally:
            return result
