from configs.flask_config import db, ma


class UsuarioPerfil(db.Model):
    __table_args__ = {"schema": "evaluationroom", 'extend_existing': True}
    __tablename__ = 'usuarioperfil'

    idperfil = db.Column(db.Integer, primary_key=True)
    idusuario = db.Column(db.Integer, db.ForeignKey('evaluationroom.usuario.idusuario'), primary_key=True)


class UsuarioPerfilSchema(ma.Schema):
    class Meta:
        fields = ('idperfil', 'idusuario')
