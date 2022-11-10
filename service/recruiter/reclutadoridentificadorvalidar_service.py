from configs.flask_config import db
from objects.usuario import Usuario
from objects.usuario_perfil import UsuarioPerfil


class ReclutadorIdentificadorValidarService():

    def valida_email_reclutador(self, email):
        usuario = db.session.query(Usuario
                    ).filter(Usuario.correoelectronico==email,
                             Usuario.activo==True,
                             db.or_(UsuarioPerfil.idperfil==1, UsuarioPerfil.idperfil==2, UsuarioPerfil.idperfil==3)
                    ).outerjoin(UsuarioPerfil,
                        UsuarioPerfil.idusuario == Usuario.idusuario
                    )

        if usuario.count():
            print('Se encontró reclutador con el correo electronico {}'.format(email))
            return True, 'Existe reclutador', usuario.one()
        print('No existe reclutador con el correo electronico {}'.format(email))
        return False, 'No existe reclutador.', None
