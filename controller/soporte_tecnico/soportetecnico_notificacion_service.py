from datetime import datetime
from configs.resources import db, text
from configs.logging import logger
import json
import pytz


class SoporteTecnicoNotificacionService():

    def guardar_mensaje_error_candidato(self, correo_electronico, observacion, detalle=None):
        """
        Descripción:
            Agregar un mensaje de error ocurrido durante la evaluación.
        Input:
            - correo_electronico:str Correo electrónico del candidato.
            - observacion:str Mensaje de error ocurrido.
            - detalle:str Detalle del error ocurrido.
        Output:
            - Indicador: Indicador True si el error fue reportado; False, si no se pudo almacenar.
        """
        result = None
        try:
            # detalle = 'NULL' if detalle is None else f"'{detalle}'"
            detalle_json = json.dumps(detalle)
            zona_horaria_peru = pytz.timezone('America/Lima')
            timestamp = datetime.now(zona_horaria_peru).strftime('%Y-%m-%d %H:%M:%S%z')
            
            sql_query = """
                INSERT INTO evaluationroom.soportetecnico_notificacion
                (correoelectronico, fecharegistro, observacion, detalle)
                VALUES
                (:correo_electronico, :timestamp, :observacion, :detalle)
                RETURNING 1
            """

            # Configura los valores de los parámetros
            params = {
                'correo_electronico': correo_electronico,
                'timestamp': timestamp,
                'observacion': observacion,
                'detalle': detalle_json
            }
            
            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response = db.execute(text(sql_query), params)
            db.commit()
            response = response.fetchone()[0]

            logger.debug("Notificación del error inserted.", response=response)
            result, code, message = response, 200, 'Se registró notificación del error en base de datos.'
        except Exception as e:
            code, message = 503, f'Error al registrar notificación de error. {e}'
        finally:
            logger.debug("Notificación del error inserted.", message=message)
            return result, code, message
