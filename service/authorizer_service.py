from configs.flask_config import db
from objects.login_user import LoginUser
from service.recruiter.reclutadoridentificadorvalidar_service import ReclutadorIdentificadorValidarService
from objects.usuario import Usuario, UsuarioSchema

reclutadoridentificadorvalidar_service = ReclutadorIdentificadorValidarService()
usuario_schema = UsuarioSchema()

class AuthorizerService():

    def validate_recruiter_identify(self, token, email):
        if email and token:
            email_valido, mensaje, usuario = reclutadoridentificadorvalidar_service.valida_email_reclutador(email)
            if email_valido:
                valido = self.validar_token_recruiter(token, usuario.idusuario)
                if valido:
                    return True, 'Usuario valido', 200, usuario.idusuario
                return False, 'Operación no valida.', 403, None
            return False, mensaje, 404, None
        return False, 'Usuario no valido.', 404, None
    
    def validate_recruiter_active(self, token, email):
        if email and token:
            email_valido, mensaje, usuario = reclutadoridentificadorvalidar_service.valida_email_reclutador(email)
            if email_valido:
                return True, 'Usuario valido', 200, usuario_schema.dump(usuario)
            return False, mensaje, 404, None
        return False, 'Usuario no valido.', 404, None
    
    def validar_token_recruiter(self, hash, idusuario):
        if hash:
            return db.session.query(LoginUser
                ).filter(LoginUser.hash == hash,
                         LoginUser.date_logout == None,
                         LoginUser.iduser == idusuario
                         ).first()
        return False

    def validate_token(self, token):
        if token:
            return True
        return False
