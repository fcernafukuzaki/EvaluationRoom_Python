from configs.resources import db, text
from configs.logging import logger

# from configs.resources import db
# from objects.perfil import Perfil, PerfilSchema

# perfil_schema = PerfilSchema()
# perfiles_schema = PerfilSchema(many=True)

class PerfilesService():
    """
    Acceso a los datos de los perfiles.
    """

    def get_perfiles(self):
        """
        Descripción:
            Retornar datos de los perfiles de acceso al sistema.
        Input:
            - None.
        Output:
            - data
        """
        result = None
        try:
            sql_query = f"""
            SELECT p.idperfil, p.nombre
            FROM evaluationroom.perfil p
            ORDER BY p.idperfil
            """

            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            perfiles = db.execute(text(sql_query))

            # Resultado en formato de lista
            data = []

            for row in perfiles:
                data_perfil = dict()
                data_perfil['idPerfil'] = row.idperfil
                data_perfil['nombre'] = row.nombre
                data.append(data_perfil)

            logger.debug("Response from perfiles.")

            if int(perfiles.rowcount) > 0:
                result, code, message = data, 200, 'Se encontró perfiles.'
            else:
                code, message = 404, 'No existen perfiles.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de perfiles en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message
    

    def get_perfil(self, uid):
        """
        Descripción:
            Retornar datos de un perfil.
        Input:
            - uid:int Identificador del perfil.
        Output:
            - data
        """
        result = None
        try:
            sql_query = f"""
            SELECT p.idperfil, p.nombre
            FROM evaluationroom.perfil p
            WHERE p.idperfil={uid}
            """

            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            perfil = db.execute(text(sql_query))

            # Formatear el resultado en formato JSON
            data = {
                'idperfil': None,
                'nombre': None,
            }

            for row in perfil:
                data['idPerfil'] = row.idperfil
                data['nombre'] = row.nombre
            
            logger.debug("Response from perfil.", uid=uid)

            if int(perfil.rowcount) > 0:
                result, code, message = data, 200, 'Se encontró perfil.'
            else:
                code, message = 404, 'No existe perfil.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de perfil {uid} en base de datos {e}'
        finally:
            logger.info("Response from perfil.", uid=uid, message=message)
            return result, code, message
    

    def add_perfil(self, nombre):
        """
        Descripción:
            Agregar un nuevo perfil.
        Input:
            - nombre:str Nombre del perfil.
        Output:
            - id: Identificador del perfil.
        """
        result = None
        try:
            sql_query = f"""
            INSERT INTO evaluationroom.perfil
            (nombre)
            VALUES
            ('{nombre}')
            RETURNING idperfil
            """
            
            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            new_perfil = db.execute(text(sql_query))
            db.commit()
            new_id_perfil = new_perfil.fetchone()[0]

            logger.debug("Perfil inserted.", new_id_perfil=new_id_perfil)
            result, code, message = new_id_perfil, 200, 'Se registró perfil en base de datos.'
        except Exception as e:
            code, message = 503, f'Hubo un error al registrar perfil en base de datos {e}'
        finally:
            logger.debug("Perfil inserted.", message=message)
            return result, code, message
    

    def update_perfil(self, uid, nombre):
        """
        Descripción:
            Actualizar datos de un perfil.
        Input:
            - uid:int Identificador del perfil.
            - nombre:str Nombre del perfil.
        Output:
            - id: Identificador del perfil.
        """
        result = None
        try:
            sql_query = f"""
            UPDATE evaluationroom.perfil
            SET nombre='{nombre}'
            WHERE idperfil={uid}
            """
            
            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            update_perfil = db.execute(text(sql_query))
            db.commit()

            logger.debug("Perfil updated.", id_perfil=uid)
            result, code, message = uid, 200, 'Se actualizó perfil en base de datos.'
        except Exception as e:
            code, message = 503, f'Hubo un error al actualizar perfil en base de datos {e}'
        finally:
            logger.debug("Perfil updated.", message=message)
            return result, code, message
