from configs.flask_config import db, ma
from .usuario_perfil import UsuarioPerfil, UsuarioPerfilSchema


class Usuario(db.Model):
    __table_args__ = {"schema": "evaluationroom"}
    __tablename__ = 'usuario'

    idusuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    correoelectronico = db.Column(db.String())
    activo = db.Column(db.Boolean())

    perfiles = db.relationship('UsuarioPerfil', lazy="dynamic",
                             primaryjoin='and_(Usuario.idusuario==UsuarioPerfil.idusuario)')


class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('idusuario', 'activo', 'perfiles')

    perfiles = ma.Nested(UsuarioPerfilSchema, many=True)
