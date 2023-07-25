import json
from configs.resources import db, text
from configs.logging import logger


class UsuarioValidarService():
    """
    Validar que un usuario (reclutador) está registrado y se encuentra activo para ingresar al sistema.
    """

    def get_data_recruiter(self, email):
        """
        Descripción:
            Retornar datos del reclutador activo a través del correo electrónico.
        Input:
            - email: correo electrónico.
        Output:
            - flag: [True, False] Indicador si existe datos. 
            - message: Mensaje de salida.
            - data: Objeto.
        """
        sql_query = f"""
        SELECT u.idusuario, u.activo, u.nombre, u.correoelectronico, u.idempresa, e.nombre, up.idperfil
        FROM evaluationroom.usuario u
        INNER JOIN evaluationroom.empresa e ON e.idempresa=u.idempresa
        INNER JOIN evaluationroom.usuarioperfil up ON u.idusuario=up.idusuario
        WHERE u.correoelectronico='{email}'
        AND u.activo=True
        AND (up.idperfil=2 OR up.idperfil=3)
        """

        # Ejecutar la consulta SQL y obtener los resultados en un dataframe
        reclutador = db.execute(text(sql_query))

        if int(reclutador.rowcount) > 0:
            logger.info('Se encontró reclutador con el correo electronico.', email=email)

            # Formatear el resultado en formato JSON
            data = {
                'idusuario': None,
                'correoelectronico': None,
                'perfiles': []
            }

            for row in reclutador:
                data['idusuario'] = row.idusuario
                data['correoelectronico'] = row.correoelectronico
                data['empresa'] = [{'idempresa': row.idempresa, 'nombre': row.nombre}]
                perfil = {
                    'idusuario': row.idusuario,
                    'idperfil': row.idperfil
                }
                data['perfiles'].append(perfil)

            # json_data = json.dumps(data)
            # print(json_data)
        
            return True, 'Existe reclutador', data
        logger.info('No existe reclutador con el correo electronico.', email=email)
        return False, 'No existe reclutador.', None


    def get_data_administrador(self, email):
        """
        Descripción:
            Retornar datos del administrador activo a través del correo electrónico.
        Input:
            - email: correo electrónico.
        Output:
            - flag: [True, False] Indicador si existe datos. 
            - message: Mensaje de salida.
            - data: Objeto.
        """
        sql_query = f"""
        SELECT u.idusuario, u.activo, u.nombre, u.correoelectronico, up.idperfil
        FROM evaluationroom.usuario u
        INNER JOIN evaluationroom.usuarioperfil up ON u.idusuario=up.idusuario
        WHERE u.correoelectronico='{email}'
        AND u.activo=True
        AND up.idperfil=1
        """

        # Ejecutar la consulta SQL y obtener los resultados en un dataframe
        administrador = db.execute(text(sql_query))

        if int(administrador.rowcount) > 0:
            logger.info('Se encontró administrador con el correo electronico.', email=email)

            # Formatear el resultado en formato JSON
            data = {
                'idusuario': None,
                'correoelectronico': None,
                'perfiles': []
            }

            for row in administrador:
                data['idusuario'] = row.idusuario
                data['correoelectronico'] = row.correoelectronico
                perfil = {
                    'idusuario': row.idusuario,
                    'idperfil': row.idperfil
                }
                data['perfiles'].append(perfil)
        
            return True, 'Existe administrador', data
        logger.info('No existe administrador con el correo electronico.', email=email)
        return False, 'No existe administrador.', None
    

    def get_data(self, email):
        """
        Descripción:
            Retornar datos de un usuario activo a través del correo electrónico.
        Input:
            - email: correo electrónico.
        Output:
            - data
        """
        # Validar si es reclutador
        flag, message, data = self.get_data_recruiter(email)

        if flag:
            return flag, message, data
            
        # Validar si es administrador
        flag, message, data = self.get_data_administrador(email)

        if flag:
            return flag, message, data

        logger.info('No existe reclutador con el correo electronico.', email=email)
        return False, 'No existe reclutador.', None
    

    def is_authorized(self, hash, idusuario):
        """
        Descripción:
            Validar que un usuario está autorizado a ingresar, 
            se encuentra activo a través del correo electrónico y su
            hash no ha sido utilizado anteriormente.
        Input:
            - hash: hash recuperado por servicio de autenticación.
            - idusuario: Identificador de usuario.
        Output:
            - boolean
        """
        sql_query = f"""
        SELECT iduser, hash, date_login, email
        FROM evaluationroom.login_user
        WHERE hash='{hash}'
        AND date_logout IS NULL
        AND iduser={idusuario}
        """
        login_user = db.execute(text(sql_query))
        # print(int(login_user.rowcount))
            
        if int(login_user.rowcount) > 0:
            return True
        return False
    

    def validate_hash(self, hash):
        """
        Descripción:
            Validar que un hash no está volviendo a ser utilizado.
        Input:
            - hash: hash recuperado por servicio de autenticación.
        Output:
            - data
        """
        if hash:
            sql_query = f"""
            SELECT iduser, hash, date_login, email
            FROM evaluationroom.login_user
            WHERE hash='{hash}'
            AND date_logout IS NULL
            AND iduser > 0
            """
            login_user = db.execute(text(sql_query))
            
            # Formatear el resultado en formato JSON
            data = {
                'iduser': None,
                'hash': None,
                'email': None,
            }
            
            for row in login_user:
                data['iduser'] = row.iduser
                data['hash'] = row.hash
                data['email'] = row.email

            return data
        else:
            return None
