from configs.logging import logger
from authorization.repository.user_access_repository import UserAccessRepository


useraccess_repository = UserAccessRepository()


class UsuarioValidarService():
    """
    Validar que un usuario (reclutador) está registrado y se encuentra activo para ingresar al sistema.
    """

    def get_data(self, email:str):
        """
        Descripción:
            Retornar datos de un usuario activo a través del correo electrónico.
        Input:
            - email: correo electrónico.
        Output:
            - data
        """
        # Validar si es reclutador
        flag, message, data = useraccess_repository.get_data_recruiter(email)

        if flag:
            return flag, message, data
            
        # Validar si es administrador
        flag, message, data = useraccess_repository.get_data_administrador(email)

        if flag:
            return flag, message, data

        logger.info('No existe reclutador con el correo electronico.', email=email)
        return False, 'No existe reclutador.', None
