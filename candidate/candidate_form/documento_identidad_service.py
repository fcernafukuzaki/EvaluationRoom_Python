from configs.resources import db, text
from configs.logging import logger


class DocumentoIdentidadService():
    
    def get_documentos_identidad(self):
        """ 
        Descripción:
            Obtener la lista de documentos de identidad.
        Input:
            - None.
        Output:
            - data: Lista de documentos de identidad.
        """
        result = None
        try:
            sql_query = f"""
            SELECT iddocumentoidentidad, nombre
            FROM evaluationroom.documentoidentidad
            ORDER BY iddocumentoidentidad
            """

            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))

            # Resultado en formato de lista
            data = []

            for row in response_database:
                obj_data = dict()
                obj_data['iddocumentoidentidad'] = row.iddocumentoidentidad
                obj_data['nombre'] = row.nombre
                data.append(obj_data)
            
            logger.debug("Response from documentoidentidad.")

            if int(response_database.rowcount) > 0:
                result, code, message = data, 200, 'Se encontró documentos de identidad.'
            else:
                code, message = 404, 'No existen documentos de identidad.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de los documentos de identidad en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message
