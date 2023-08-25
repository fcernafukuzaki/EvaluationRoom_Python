from configs.resources import db
from .usuario_validar_service import UsuarioValidarService

usuariovalidar_service = UsuarioValidarService()

class AuthorizerService():

    def validate_recruiter_identify(self, token, email):
        if email and token:
            email_valido, mensaje, usuario = usuariovalidar_service.get_data(email)
            if email_valido:
                valido = self.validate_token_recruiter(token, usuario.get("idusuario"))
                if valido:
                    return True, 'Usuario valido.', 200, usuario.get("idusuario")
                return False, 'Operación no valida.', 403, None
            return False, mensaje, 404, None
        return False, 'Usuario no valido.', 404, None
    

    def validate_recruiter_active(self, token, email):
        if email and token:
            email_valido, mensaje, usuario = usuariovalidar_service.get_data(email)
            if email_valido:
                return True, 'Usuario valido.', 200, usuario
            return False, mensaje, 404, None
        return False, 'Usuario no valido.', 404, None
    

    def validate_token_recruiter(self, hash, idusuario):
        if hash:
            return usuariovalidar_service.is_authorized(hash, idusuario)
        return False

    
    def validate_token(self, token):
        if token:
            return True
        return False
    

    def validate_candidate(self, token, email):
        if email and token:
            return True, 'Operación valida.', 200, None
        return False, 'Operación no valida.', 403, None
