from configs.resources import db, text
from configs.logging import logger


class EstadoCivilService():
    
    def get_estados_civil(self):
        """ 
        Descripción:
            Obtener la lista de estados civil.
        Input:
            - None.
        Output:
            - data: Lista de estados civil.
        """
        result = None
        try:
            sql_query = f"""
            SELECT idestadocivil, nombre
            FROM evaluationroom.estadocivil
            ORDER BY idestadocivil
            """

            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))

            # Resultado en formato de lista
            data = []

            for row in response_database:
                obj_data = dict()
                obj_data['idestadocivil'] = row.idestadocivil
                obj_data['nombre'] = row.nombre
                data.append(obj_data)
            
            logger.debug("Response from estado civil.")

            if int(response_database.rowcount) > 0:
                result, code, message = data, 200, 'Se encontró estados civil.'
            else:
                code, message = 404, 'No existen estados civil.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de los estados civil en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message
