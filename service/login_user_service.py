from datetime import datetime, timezone
from configs.resources import db, text


class LoginUserService():
    """
    Monitorear actividad de acceso al sistema.
    """

    def add_login_user(self, id_user, hash, email):
        """
        Descripción:
            Registrar intento de acceso al sistema.
        Input:
            - id_user: Identificador de usuario.
            - hash: hash recuperado por servicio de autenticación.
            - email: correo electrónico.
        Output:
            - data
        """
        try:
            date_login = datetime.now(timezone.utc)
            sql_query = f"""
            INSERT INTO evaluationroom.login_user 
            (iduser, hash, date_login, email)
            VALUES
            ({id_user}, '{hash}', '{date_login}', '{email}')
            """
            new_login_user = db.execute(text(sql_query))
            db.commit()
            print(f"User loged ({email}) inserted")
            
            message = 'Se registró login en base de datos.'
            return new_login_user, 200, message
        except Exception as e:
            message = f'Hubo un error al registrar login en base de datos {e}'
            return None, 503, message
