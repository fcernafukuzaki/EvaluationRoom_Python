from configs.resources import db, text
from configs.logging import logger


class SexoService():
    
    def get_sexos(self):
        """ 
        Descripción:
            Obtener la lista de géneros.
        Input:
            - None.
        Output:
            - data: Lista de géneros.
        """
        result = None
        try:
            sql_query = f"""
            SELECT idsexo, nombre
            FROM evaluationroom.sexo
            ORDER BY idsexo
            """

            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))

            # Resultado en formato de lista
            data = []

            for row in response_database:
                obj_data = dict()
                obj_data['idsexo'] = row.idsexo
                obj_data['nombre'] = row.nombre
                data.append(obj_data)
            
            logger.debug("Response from género.")

            if int(response_database.rowcount) > 0:
                result, code, message = data, 200, 'Se encontró género.'
            else:
                code, message = 404, 'No existen género.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de los género en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message
