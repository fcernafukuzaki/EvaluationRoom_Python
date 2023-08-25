from configs.resources import db, text
from configs.logging import logger


class MensajeProcesoseleccionCandidatoService:
    def _consultar_mensajes_error(self, type:str):
        """Obtener los mensajes de error."""
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

            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))

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

            if int(response_database.rowcount) > 0:
                result, code, message = data, 200, "Se encontró mensajes de error."
            else:
                code, message = 404, "No existen mensajes de error."
        except Exception as e:
            code, message = 503, f"Hubo un error al obtener datos de mensajes de error en base de datos {e}",
        finally:
            logger.info(message)
            return result, code, message


    def obtener_mensajes_error(self, type):
        result, code, message = self._consultar_mensajes_error(type)
        return result, code, message
