from configs.resources import db, text
from configs.logging import logger


class PsychologicalTestService():
    
    def get_psychologicaltests(self):
        """ 
        Descripción:
            Obtener la lista de tests psicológicos.
        Input:
            - None.
        Output:
            - data: Lista de tests psicológicos.
        """
        result = None
        try:
            sql_query = f"""
            SELECT idtestpsicologico, nombre, cantidadpreguntas
            FROM evaluationroom.testpsicologico
            ORDER BY idtestpsicologico
            """

            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))

            # Resultado en formato de lista
            data = []

            for row in response_database:
                obj_data = dict()
                obj_data['idtestpsicologico'] = row.idtestpsicologico
                obj_data['nombre'] = row.nombre
                obj_data['cantidadpreguntas'] = row.cantidadpreguntas
                data.append(obj_data)
            
            logger.debug("Response from tests psicológicos.")

            if int(response_database.rowcount) > 0:
                result, code, message = data, 200, 'Se encontró tests psicológicos.'
            else:
                code, message = 404, 'No existen género.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de los tests psicológicos en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message
