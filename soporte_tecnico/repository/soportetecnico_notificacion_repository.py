from datetime import datetime
import pytz
import json
from configs.resources import db, text
from configs.logging import logger


class SoporteTecnicoNotificacionRepository():
    
    def add(self, email:str, observacion:str, detalle=None):
        """ 
        Descripción:
            Agregar un mensaje de error ocurrido durante la evaluación.
        Input:
            - email:str Correo electrónico del candidato.
            - observacion:str Mensaje de error ocurrido.
            - detalle:str Detalle del error ocurrido.
        
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result:int Valor 1 si se registró la notificación.
        """
        result = None
        try:
            detalle_json = json.dumps(detalle)
            zona_horaria_peru = pytz.timezone('America/Lima')
            timestamp = datetime.now(zona_horaria_peru).strftime('%Y-%m-%d %H:%M:%S%z')
            
            sql_query = '''INSERT INTO evaluationroom.soportetecnico_notificacion \
                (correoelectronico, fecharegistro, observacion, detalle) \
                VALUES \
                (:email, :timestamp, :observacion, :detalle) \
                RETURNING 1 \
            '''

            # Configura los valores de los parámetros
            params = {
                'email': email,
                'timestamp': timestamp,
                'observacion': observacion,
                'detalle': detalle_json
            }

            # Ejecutar la consulta SQL
            response_database = db.execute(text(sql_query), params)
            db.commit()
            response = response_database.fetchone()[0]
            logger.debug("Notificación del error inserted.", response=response)
            result, flag, message = response, True, 'Se registró notificación del error en base de datos.'
        except Exception as e:
            logger.error("Error al registrar notificación del error.", error=e)
            db.rollback()
            flag, message = False, f'Error al registrar notificación de error. {e}'
        finally:
            logger.info(message)
            return flag, message, result
