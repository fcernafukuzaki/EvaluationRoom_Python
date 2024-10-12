from configs.resources import db, text
from configs.logging import logger


class UserAccessRepository():
    """
    Validar que un usuario (reclutador) está registrado y se encuentra activo para ingresar al sistema.
    """
    
    def get_data_recruiter(self, email:str):
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
        
            return True, 'Existe reclutador', data
        logger.info('No existe reclutador con el correo electronico.', email=email)
        return False, 'No existe reclutador.', None


    def get_data_administrador(self, email:str):
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
