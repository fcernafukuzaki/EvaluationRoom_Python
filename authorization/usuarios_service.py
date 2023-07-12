from configs.resources import db, text
# from configs.resources import db
# from objects.usuario import Usuario, UsuarioAccesosGestionSchema, UsuarioInfoSchema
# from objects.usuario_perfil import UsuarioPerfil
from configs.logging import logger

# usuario_info_schema = UsuarioInfoSchema()
# usuarios_schema = UsuarioAccesosGestionSchema(many=True)

class UsuariosService():
    """
    Acceso a los datos de los usuarios o de un usuario.
    """

    def get_usuarios(self):
        """
        Descripción:
            Retornar datos de los usuarios que tienen acceso al sistema.
        Input:
            - None.
        Output:
            - data
        """
        result = None
        try:
            sql_query = f"""
            SELECT u.idusuario, u.activo, u.nombre, u.correoelectronico
            FROM evaluationroom.usuario u
            ORDER BY u.idusuario
            """

            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            usuarios = db.execute(text(sql_query))

            # Resultado en formato de lista
            data = []

            for row in usuarios:
                data_usuario = dict()
                data_usuario['idUsuario'] = row.idusuario
                data_usuario['activo'] = row.activo
                data_usuario['correoElectronico'] = row.correoelectronico
                data_usuario['nombre'] = row.nombre
                data.append(data_usuario)
            
            logger.debug("Response from usuarios.")

            if int(usuarios.rowcount) > 0:
                result, code, message = data, 200, 'Se encontró usuarios.'
            else:
                code, message = 404, 'No existen usuarios.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de usuarios en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message
    

    def get_usuario(self, uid):
        """
        Descripción:
            Retornar datos de un usuario.
        Input:
            - uid:int Identificador del usuario.
        Output:
            - data
        """
        result = None
        try:
            sql_query = f"""
            SELECT u.idusuario, u.activo, u.nombre, u.correoelectronico, up.idperfil, p.nombre AS "perfil_nombre"
            FROM evaluationroom.usuario u
            INNER JOIN evaluationroom.usuarioperfil up ON u.idusuario=up.idusuario
            INNER JOIN evaluationroom.perfil p ON p.idperfil=up.idperfil
            WHERE u.idusuario={uid}
            """

            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            usuario = db.execute(text(sql_query))

            # Formatear el resultado en formato JSON
            data = {
                'idUsuario': None,
                'activo': None,
                'nombre': None,
                'correoElectronico': None,
                'perfiles': []
            }

            for row in usuario:
                data['idUsuario'] = row.idusuario
                data['activo'] = row.activo
                data['nombre'] = row.nombre
                data['correoElectronico'] = row.correoelectronico
                perfil = {
                    'idUsuario': row.idusuario,
                    'idPerfil': row.idperfil,
                    'nombre': row.perfil_nombre
                }
                data['perfiles'].append(perfil)

            logger.debug("Response from usuario.", uid=uid)
            
            if int(usuario.rowcount) > 0:
                result, code, message = data, 200, 'Se encontró usuario.'
            else:
                code, message = 404, 'No existe usuario.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de usuario {uid} en base de datos {e}'
        finally:
            logger.info("Response from usuario.", uid=uid, message=message)
            return result, code, message
    

    def add_usuario(self, nombre, email, activo):
        """
        Descripción:
            Agregar un nuevo usuario.
        Input:
            - nombre:str Nombre del usuario.
            - email:str Correo electrónico del usuario.
            - activo:bool [True, False] Activo o no activo.
        Output:
            - id: Identificador del usuario.
        """
        result = None
        try:
            sql_query = f"""
            INSERT INTO evaluationroom.usuario
            (nombre, correoelectronico, activo)
            VALUES
            ('{nombre}', '{email}', '{activo}')
            RETURNING idusuario
            """
            
            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            new_usuario = db.execute(text(sql_query))
            db.commit()
            new_id_usuario = new_usuario.fetchone()[0]

            logger.debug("Usuario inserted.", new_id_usuario=new_id_usuario)
            result, code, message = new_id_usuario, 200, 'Se registró usuario en base de datos.'
        except Exception as e:
            code, message = 503, f'Hubo un error al registrar usuario en base de datos {e}'
        finally:
            logger.debug("Usuario inserted.", message=message)
            return result, code, message
    

    def update_usuario(self, uid, nombre, email, activo):
        """
        Descripción:
            Actualizar datos de un usuario.
        Input:
            - uid:int Identificador del usuario.
            - nombre:str Nombre del usuario.
            - email:str Correo electrónico del usuario.
            - activo:bool [True, False] Activo o no activo.
        Output:
            - id: Identificador del usuario.
        """
        result = None
        try:
            sql_query = f"""
            UPDATE evaluationroom.usuario
            SET nombre='{nombre}', 
            correoelectronico='{email}', 
            activo='{activo}'
            WHERE idusuario={uid}
            """

            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            usuario = db.execute(text(sql_query))
            db.commit()

            logger.debug("Usuario updated.", id_usuario=uid)
            result, code, message = uid, 200, 'Se actualizó usuario en base de datos.'
        except Exception as e:
            code, message = 503, f'Hubo un error al actualizar usuario en base de datos {e}'
        finally:
            logger.debug("Usuario updated.", message=message)
            return result, code, message
    

    # def delete_perfiles(self, uid, idperfiles):
    #     result = None
    #     try:
    #         for perfil in idperfiles:
    #             usuario_perfil = UsuarioPerfil.query.get((uid, perfil))
    #             if usuario_perfil:
    #                 db.session.delete(usuario_perfil)
    #                 db.session.commit()
    #         result, code, message = uid, 200, 'Se eliminó perfil en base de datos.'
    #     except Exception as e:
    #         code, message = 503, f'Hubo un error al eliminar perfil en base de datos {e}'
    #     finally:
    #         print(message)
    #         return result, code, message
    
    # def add_perfiles(self, uid, perfiles):
    #     result = None
    #     try:
    #         for perfil in perfiles:
    #             usuario_perfil = UsuarioPerfil(uid, perfil['idPerfil'])
    #             db.session.add(usuario_perfil)
    #             db.session.commit()
            
    #         result, code, message = uid, 200, f'Se registró perfiles al usuario {uid} en base de datos.'
    #     except Exception as e:
    #         code, message = 503, f'Hubo un error al registrar perfiles al usuario {uid} en base de datos {e}'
    #     finally:
    #         print(message)
    #         return result, code, message
