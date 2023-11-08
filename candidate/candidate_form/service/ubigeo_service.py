from configs.resources import db, text
from configs.logging import logger


class UbigeoService():
    
    def get_countries(self):
        """ 
        Descripción:
            Obtener la lista de paises.
        Input:
            - None.
        Output:
            - data: Lista de paises.
        """
        result = None
        try:
            sql_query = f"""
            SELECT idpais, nombre
            FROM evaluationroom.pais
            ORDER BY idpais
            """

            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))

            # Resultado en formato de lista
            data = []

            for row in response_database:
                obj_data = dict()
                obj_data['idpais'] = row.idpais
                obj_data['nombre'] = row.nombre
                data.append(obj_data)
            
            logger.debug("Response from paises.")

            if int(response_database.rowcount) > 0:
                result, code, message = data, 200, 'Se encontró paises.'
            else:
                code, message = 404, 'No existen paises.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de los paises en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message

    
    def get_departamentos_by_country(self, id_country):
        """ 
        Descripción:
            Obtener la lista de departamentos por país.
        Input:
            - id_country: Identificador del país.
        Output:
            - data: Lista de departamentos.
        """
        result = None
        try:
            sql_query = f"""
            SELECT idpais, iddepartamento, nombre
            FROM evaluationroom.departamento
            WHERE idpais={id_country}
            ORDER BY idpais, iddepartamento
            """

            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))

            # Resultado en formato de lista
            data = []

            for row in response_database:
                obj_data = dict()
                obj_data['idpais'] = row.idpais
                obj_data['iddepartamento'] = row.iddepartamento
                obj_data['nombre'] = row.nombre
                data.append(obj_data)
            
            logger.debug("Response from departamentos.")

            if int(response_database.rowcount) > 0:
                result, code, message = data, 200, 'Se encontró departamentos.'
            else:
                code, message = 404, 'No existen departamentos.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de los departamentos en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message
    
    
    def get_provincias_by_ids(self, id_country, id_departamento):
        """ 
        Descripción:
            Obtener la lista de provincias por departamentos.
        Input:
            - id_country: Identificador del país.
            - id_departamento: Identificador del departamento.
        Output:
            - data: Lista de provincias.
        """
        result = None
        try:
            sql_query = f"""
            SELECT idpais, iddepartamento, idprovincia, nombre
            FROM evaluationroom.provincia
            WHERE idpais={id_country}
            AND iddepartamento={id_departamento}
            ORDER BY idpais, iddepartamento, idprovincia
            """

            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))

            # Resultado en formato de lista
            data = []

            for row in response_database:
                obj_data = dict()
                obj_data['idpais'] = row.idpais
                obj_data['iddepartamento'] = row.iddepartamento
                obj_data['idprovincia'] = row.idprovincia
                obj_data['nombre'] = row.nombre
                data.append(obj_data)
            
            logger.debug("Response from provincias.")

            if int(response_database.rowcount) > 0:
                result, code, message = data, 200, 'Se encontró provincias.'
            else:
                code, message = 404, 'No existen provincias.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de las provincias en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message
    
    
    def get_distritos_by_ids(self, id_country, id_departamento, id_provincia):
        """ 
        Descripción:
            Obtener la lista de distritos por provincias.
        Input:
            - id_country: Identificador del país.
            - id_departamento: Identificador del departamento.
            - id_provincia: Identificador de provincia.
        Output:
            - data: Lista de distritos.
        """
        result = None
        try:
            sql_query = f"""
            SELECT idpais, iddepartamento, idprovincia, iddistrito, nombre
            FROM evaluationroom.distrito
            WHERE idpais={id_country}
            AND iddepartamento={id_departamento}
            AND idprovincia={id_provincia}
            ORDER BY idpais, iddepartamento, idprovincia, iddistrito
            """

            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))

            # Resultado en formato de lista
            data = []

            for row in response_database:
                obj_data = dict()
                obj_data['idpais'] = row.idpais
                obj_data['iddepartamento'] = row.iddepartamento
                obj_data['idprovincia'] = row.idprovincia
                obj_data['iddistrito'] = row.iddistrito
                obj_data['nombre'] = row.nombre
                data.append(obj_data)
            
            logger.debug("Response from provincias.")

            if int(response_database.rowcount) > 0:
                result, code, message = data, 200, 'Se encontró distritos.'
            else:
                code, message = 404, 'No existen distritos.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de los distritos en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message
