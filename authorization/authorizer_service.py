from configs.resources import db
# from objects.login_user import LoginUser
from .reclutadoridentificadorvalidar_service import ReclutadorIdentificadorValidarService
# from objects.usuario import Usuario, UsuarioSchema

reclutadoridentificadorvalidar_service = ReclutadorIdentificadorValidarService()
# usuario_schema = UsuarioSchema()

class AuthorizerService():

    def validate_recruiter_identify(self, token, email):
        if email and token:
            email_valido, mensaje, usuario = reclutadoridentificadorvalidar_service.get_data(email)
            if email_valido:
                valido = self.validate_token_recruiter(token, usuario.get("idusuario"))
                if valido:
                    return True, 'Usuario valido.', 200, usuario.get("idusuario")
                return False, 'Operación no valida.', 403, None
            return False, mensaje, 404, None
        return False, 'Usuario no valido.', 404, None
    

    def validate_recruiter_active(self, token, email):
        if email and token:
            email_valido, mensaje, usuario = reclutadoridentificadorvalidar_service.get_data(email)
            if email_valido:
                return True, 'Usuario valido.', 200, usuario
            return False, mensaje, 404, None
        return False, 'Usuario no valido.', 404, None
    

    def validate_token_recruiter(self, hash, idusuario):
        if hash:
            return reclutadoridentificadorvalidar_service.is_authorized(hash, idusuario)
        return False

    
    def validate_token(self, token):
        if token:
            return True
        return False
