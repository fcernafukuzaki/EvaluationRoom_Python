from configs.resources import db, text
from configs.logging import logger


class TipoDireccionService():
    
    def get_tipos_direccion(self):
        """ 
        Descripción:
            Obtener la lista de tipos de direcciones.
        Input:
            - None.
        Output:
            - data: Lista de tipos de direcciones.
        """
        result = None
        try:
            sql_query = f"""
            SELECT idtipodireccion, nombre
            FROM evaluationroom.tipodireccion
            ORDER BY idtipodireccion
            """

            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))

            # Resultado en formato de lista
            data = []

            for row in response_database:
                obj_data = dict()
                obj_data['idtipodireccion'] = row.idtipodireccion
                obj_data['nombre'] = row.nombre
                data.append(obj_data)
            
            logger.debug("Response from tipos de direcciones.")

            if int(response_database.rowcount) > 0:
                result, code, message = data, 200, 'Se encontró tipos de direcciones.'
            else:
                code, message = 404, 'No existen género.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de los tipos de direcciones en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message
