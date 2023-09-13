import pandas as pd
from configs.resources import db, text
from configs.logging import logger


class EvaluationMessageCandidateRepository():
    
    def get_mensajes_error(self, type:str):
        """ 
        Descripción:
            Obtener los mensajes de error.
        Input:
            - type:str Tipo de mensaje de error (registro, testpsicologico).
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result: Objeto de mensajes de error.
        """
        result = None
        try:
            types = {
                'registro': [3,4,6],
                'testpsicologico': [5]
            }

            sql_query = f"SELECT id_mensaje, tipo_mensaje, mensaje \
                FROM evaluationroom.mensaje_procesoseleccion_candidato \
                WHERE SUBSTR(tipo_mensaje, 1, LENGTH('mensaje_error')) = 'mensaje_error' \
                ORDER BY id_mensaje\
            "

            # Ejecutar la consulta SQL
            response_database = db.execute(text(sql_query))

            if int(response_database.rowcount) > 0:
                # Resultado en formato de lista
                data = [
                    {
                        "id_mensaje": row.id_mensaje, 
                        "tipo_mensaje": row.tipo_mensaje,
                        "mensaje": row.mensaje,
                    }
                    for row in response_database
                    if row.id_mensaje in types.get(type)
                ]

                result, flag, message = data, True, "Se encontró mensajes de error."
            else:
                flag, message = False, "No existen mensajes de error."
        except Exception as e:
            logger.error("Error.", error=e)
            db.rollback()
            flag, message = False, f"Hubo un error al obtener datos de mensajes de error en base de datos {e}",
        finally:
            logger.info(message)
            return flag, message, result


    def get_mensaje_bienvenida(self, uid:int):
        """ 
        Descripción:
            Obtener el mensaje de bienvenida.
        Input:
            - uid:int Identificador del mensaje.
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result: Objeto de mensajes de error.
        """
        result = None
        try:
            sql_query = f"SELECT id_mensaje, tipo_mensaje, mensaje \
                FROM evaluationroom.mensaje_procesoseleccion_candidato \
                WHERE id_mensaje = '{uid}' \
                ORDER BY id_mensaje\
            "

            # Ejecutar la consulta SQL
            response_database = db.execute(text(sql_query))

            if int(response_database.rowcount) > 0:
                for row in response_database:
                    data = {
                        "id_mensaje": row.id_mensaje, 
                        "tipo_mensaje": row.tipo_mensaje,
                        "mensaje": row.mensaje,
                    }

                result, flag, message = data, True, "Se encontró mensaje de bienvenida."
            else:
                flag, message = False, "No existen mensaje de bienvenida."
        except Exception as e:
            logger.error("Error.", error=e)
            db.rollback()
            flag, message = False, f"Hubo un error al obtener datos de mensaje de bienvenida en base de datos {e}",
        finally:
            logger.info(message)
            return flag, message, result
