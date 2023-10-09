from configs.resources import db, text
from configs.logging import logger


class PerfilesRepository():
    
    def get_all(self):
        """ 
        Descripción:
            Obtener los perfiles de acceso al sistema.
        Input:
            - None.
        
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result:object Objeto.
        """
        result = None
        try:
            sql_query = "SELECT p.idperfil, p.nombre \
                FROM evaluationroom.perfil p \
                ORDER BY p.idperfil \
            "

            # Ejecutar la consulta SQL
            response_database = db.execute(text(sql_query))

            if int(response_database.rowcount) > 0:
                # Resultado en formato de lista
                data = [
                    {
                        "idPerfil": row.idperfil, 
                        "nombre": row.nombre,
                    }
                    for row in response_database
                ]

                result, flag, message = data, True, "Se encontró perfiles."
            else:
                flag, message = False, "No existen perfiles."
        except Exception as e:
            logger.error("Error al obtener datos de perfiles.", error=e)
            db.rollback()
            flag, message = False, f"Hubo un error al obtener datos de perfiles en base de datos {e}"
        finally:
            logger.info(message)
            return flag, message, result


    def get(self, uid:int):
        """ 
        Descripción:
            Obtener datos de un perfil de acceso al sistema.
        Input:
            - uid:int Identificador del perfil.
        
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result:object Objeto.
        """
        result = None
        try:
            sql_query = f"SELECT p.idperfil, p.nombre \
                FROM evaluationroom.perfil p \
                WHERE p.idperfil={uid} \
            "

            # Ejecutar la consulta SQL
            response_database = db.execute(text(sql_query))

            if int(response_database.rowcount) > 0:
                data = {
                    "idPerfil": response_database.idperfil, 
                    "nombre": response_database.nombre,
                }
                
                result, flag, message = data, True, "Se encontró perfil."
            else:
                flag, message = False, "No existen perfil."
        except Exception as e:
            logger.error("Error al obtener datos del perfil.", error=e)
            db.rollback()
            flag, message = False, f"Hubo un error al obtener datos del perfil en base de datos {e}"
        finally:
            logger.info(message)
            return flag, message, result


    def add(self, nombre:str):
        """ 
        Descripción:
            Agregar un nuevo perfil.
        Input:
            - nombre:str Nombre del perfil.
        
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result:int Identificador del perfil.
        """
        result = None
        try:
            sql_query = f"INSERT INTO evaluationroom.perfil \
                (nombre) \
                VALUES \
                ('{nombre}') \
                RETURNING idperfil \
            "

            # Ejecutar la consulta SQL
            response_database = db.execute(text(sql_query))
            db.commit()
            uid = response_database.fetchone()[0]
            logger.debug("Perfil inserted.", uid=uid)
            result, flag, message = uid, True, 'Se registró perfil en base de datos.'
        except Exception as e:
            logger.error("Error al registrar datos del perfil.", error=e)
            db.rollback()
            flag, message = False, f"Hubo un error al registrar perfil en base de datos {e}"
        finally:
            logger.info(message)
            return flag, message, result


    def update(self, uid:int, nombre:str):
        """ 
        Descripción:
            Actualizar datos de un perfil.
        Input:
            - uid:int Identificador del perfil.
            - nombre:str Nombre del perfil.
        
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result:int Identificador del perfil.
        """
        result = None
        try:
            sql_query = f"UPDATE evaluationroom.perfil \
                SET nombre='{nombre}' \
                WHERE idperfil={uid} \
            "

            # Ejecutar la consulta SQL
            db.execute(text(sql_query))
            db.commit()
            logger.debug("Perfil updated.", uid=uid)
            result, flag, message = uid, True, 'Se actualizó perfil en base de datos.'
        except Exception as e:
            logger.error("Error al actualizar datos del perfil.", error=e)
            db.rollback()
            flag, message = False, f"Hubo un error al actualizar perfil en base de datos {e}"
        finally:
            logger.info(message)
            return flag, message, result


    def assign_to(self, uid:int, perfiles=None):
        """ 
        Descripción:
            Asignar perfiles a un usuario.
        Input:
            - uid:int Identificador del usuario.
            - perfiles:list Lista de perfiles para asignar al usuario.
        
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result:int Identificador del usuario.
        """
        result = None
        try:
            # Eliminar perfiles
            sql_query = f"DELETE FROM evaluationroom.usuarioperfil \
            WHERE idusuario={uid} \
            "

            # Ejecutar la consulta SQL
            db.execute(text(sql_query))
            db.commit()
            logger.debug("Se eliminó perfiles del usuario en base de datos.", uid=uid)

            if perfiles:
                for perfil in perfiles:
                    id_perfil = perfil["idPerfil"]
                    sql_query = f"INSERT INTO evaluationroom.usuarioperfil \
                    (idperfil, idusuario) \
                    VALUES \
                    ({id_perfil}, {uid}) \
                    """

                    # Ejecutar la consulta SQL y obtener los resultados en un dataframe
                    db.execute(text(sql_query))
                    db.commit()
                    logger.debug("Se registró perfil al usuario en base de datos.", uid=uid, id_perfil=id_perfil)

            logger.debug("Perfiles asigned.", uid=uid)
            result, flag, message = uid, True, 'Se asignó perfil en base de datos.'
        except Exception as e:
            logger.error("Error al asignar perfiles.", error=e)
            db.rollback()
            flag, message = False, f"Hubo un error al asignar perfiles en base de datos {e}"
        finally:
            logger.info(message)
            return flag, message, result
