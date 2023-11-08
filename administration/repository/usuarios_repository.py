import json
import pandas as pd
from configs.resources import db, text
from configs.logging import logger


class UsuariosRepository():
    
    def get_all(self):
        """ 
        Descripción:
            Retornar datos de los usuarios que tienen acceso al sistema.
        Input:
            - None.
        
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result:object Objeto.
        """
        result = None
        try:
            sql_query = "SELECT u.idusuario, u.activo, u.nombre, u.correoelectronico, u.idempresa \
            FROM evaluationroom.usuario u \
            ORDER BY u.idusuario \
            "

            # Ejecutar la consulta SQL
            response_database = db.execute(text(sql_query))

            if int(response_database.rowcount) > 0:
                # Resultado en formato de lista
                data = [
                    {
                        'idUsuario': row.idusuario,
                        'activo': row.activo,
                        'correoElectronico': row.correoelectronico,
                        'nombre': row.nombre,
                        'idEmpresa': row.idempresa,
                    }
                    for row in response_database
                ]

                result, flag, message = data, True, 'Se encontró usuarios.'
            else:
                flag, message = False, 'No existen usuarios.'
        except Exception as e:
            logger.error("Error al obtener datos de usuarios.", error=e)
            db.rollback()
            flag, message = False, f'Hubo un error al obtener datos de usuarios en base de datos {e}'
        finally:
            logger.info(message)
            return flag, message, result


    def get(self, uid:int):
        """ 
        Descripción:
            Obtener datos de un usuario.
        Input:
            - uid:int Identificador del perfil.
        
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result:object Objeto.
        """
        result = None
        try:
            sql_query = f'SELECT u.idusuario, u.activo, u.nombre, u.correoelectronico, u.idempresa, up.idperfil, p.nombre AS "perfil_nombre" \
            FROM evaluationroom.usuario u \
            LEFT JOIN evaluationroom.usuarioperfil up ON u.idusuario=up.idusuario \
            LEFT JOIN evaluationroom.perfil p ON p.idperfil=up.idperfil \
            WHERE u.idusuario={uid} \
            '

            # Ejecutar la consulta SQL
            response_database = db.execute(text(sql_query))

            if int(response_database.rowcount) > 0:
                results = response_database.fetchall()

                # Convierte los resultados a un DataFrame de pandas
                df_results = pd.DataFrame(results)

                # Agrupar y obtener los valores únicos
                fields = ['idusuario', 'activo', 'nombre', 'correoelectronico', 'idempresa']
                df_results = df_results.groupby(fields).apply(lambda x: x[['idusuario', 'idperfil', 'perfil_nombre']].to_dict('records')).reset_index()
                fields_rename = {'idusuario': 'idUsuario', 'correoelectronico': 'correoElectronico', 'idempresa': 'idEmpresa', 0: 'perfiles'}
                df_results = df_results.rename(columns=fields_rename)
                # Convertir a JSON
                json_result = df_results.to_json(orient='records')

                json_result = json.loads(json_result)[0]
                # Actualizar los nombres de los campos dentro de "nuevo_campo"
                for item in json_result['perfiles']:
                    item['idUsuario'] = item.pop('idusuario')
                    item['idPerfil'] = item.pop('idperfil')
                    item['nombre'] = item.pop('perfil_nombre')

                data = json_result
                result, flag, message = data, True, 'Se encontró usuario.'
                logger.debug("Response from usuario.", uid=uid)
            else:
                flag, message = False, 'No existe usuario.'
        except Exception as e:
            logger.error("Error al obtener datos del usuario.", error=e)
            db.rollback()
            flag, message = False, f"Hubo un error al obtener datos del usuario en base de datos {e}"
        finally:
            logger.info(message)
            return flag, message, result


    def add(self, nombre:str, email:str, activo:bool, idempresa:int):
        """ 
        Descripción:
            Agregar un nuevo usuario.
        Input:
            - nombre:str Nombre del usuario.
            - email:str Correo electrónico del usuario.
            - activo:bool [True, False] Activo o no activo.
            - idempresa: int. Identificador de la empresa.
        
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result:int Identificador del usuario.
        """
        result = None
        try:
            sql_query = f"INSERT INTO evaluationroom.usuario \
            (nombre, correoelectronico, activo, idempresa) \
            VALUES \
            ('{nombre}', '{email}', '{activo}', {idempresa}) \
            RETURNING idusuario \
            "

            # Ejecutar la consulta SQL
            response_database = db.execute(text(sql_query))
            db.commit()
            uid = response_database.fetchone()[0]
            logger.debug("Usuario inserted.", uid=uid)
            result, flag, message = uid, True, 'Se registró usuario en base de datos.'
        except Exception as e:
            logger.error("Error al registrar datos del usuario.", error=e)
            db.rollback()
            flag, message = False, f"Hubo un error al registrar usuario en base de datos {e}"
        finally:
            logger.info(message)
            return flag, message, result


    def update(self, uid:int, nombre:str, email:str, activo:bool, idempresa:int):
        """ 
        Descripción:
            Actualizar datos de un usuario.
        Input:
            - uid:int Identificador del usuario.
            - nombre:str Nombre del usuario.
            - email:str Correo electrónico del usuario.
            - activo:bool [True, False] Activo o no activo.
            - idempresa: int. Identificador de la empresa.
        
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result:int Identificador del usuario.
        """
        result = None
        try:
            sql_query = f"UPDATE evaluationroom.usuario \
            SET nombre='{nombre}',  \
            correoelectronico='{email}', \
            activo='{activo}', \
            idempresa={idempresa} \
            WHERE idusuario={uid} \
            "

            # Ejecutar la consulta SQL
            db.execute(text(sql_query))
            db.commit()
            logger.debug("Usuario updated.", uid=uid)
            result, flag, message = uid, True, 'Se actualizó usuario en base de datos.'
        except Exception as e:
            logger.error("Error al actualizar datos del usuario.", error=e)
            db.rollback()
            flag, message = False, f"Hubo un error al actualizar usuario en base de datos {e}"
        finally:
            logger.info(message)
            return flag, message, result
