import json
from configs.resources import db, text


class ReclutadorIdentificadorValidarService():
    """
    Validar que un usuario (reclutador) está registrado y se encuentra activo para ingresar al sistema.
    """

    def get_data(self, email):
        """
        Descripción:
            Retornar datos de un usuario activo a través del correo electrónico.
        Input:
            - email: correo electrónico.
        Output:
            - data
        """
        sql_query = f"""
        SELECT u.idusuario, u.activo, u.nombre, u.correoelectronico, up.idperfil
        FROM evaluationroom.usuario u
        INNER JOIN evaluationroom.usuarioperfil up ON u.idusuario=up.idusuario
        WHERE u.correoelectronico='{email}'
        AND u.activo=True
        AND (up.idperfil=1 OR up.idperfil=2 OR up.idperfil=3)
        """

        # Ejecutar la consulta SQL y obtener los resultados en un dataframe
        usuario = db.execute(text(sql_query))

        # Formatear el resultado en formato JSON
        data = {
            'idusuario': None,
            'correoelectronico': None,
            'perfiles': []
        }

        for row in usuario:
            data['idusuario'] = row.idusuario
            data['correoelectronico'] = row.correoelectronico
            perfil = {
                'idusuario': row.idusuario,
                'idperfil': row.idperfil
            }
            data['perfiles'].append(perfil)

        json_data = json.dumps(data)
        print(json_data)
        
        if int(usuario.rowcount) > 0:
            print('Se encontró reclutador con el correo electronico {}'.format(email))
            return True, 'Existe reclutador', data
        print('No existe reclutador con el correo electronico {}'.format(email))
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
        print(int(login_user.rowcount))
            
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
