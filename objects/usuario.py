from configs.resources import db, ma
from objects.usuario_perfil import UsuarioPerfil, UsuarioPerfilSchema, UsuarioPerfilInfoSchema


class Usuario(db.Model):
    __table_args__ = {"schema": "evaluationroom", 'extend_existing': True}
    __tablename__ = 'usuario'

    idusuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    correoelectronico = db.Column(db.String())
    activo = db.Column(db.Boolean())

    perfiles = db.relationship('UsuarioPerfil', lazy="dynamic",
                             primaryjoin='and_(Usuario.idusuario==UsuarioPerfil.idusuario)',
                             order_by="and_(UsuarioPerfil.idusuario,UsuarioPerfil.idperfil)")

    def __init__(self, id_usuario=None, nombre=None, email=None, activo=False):
        self.idusuario = id_usuario
        self.nombre = nombre
        self.correoelectronico = email
        self.activo = activo


class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('idusuario', 'activo', 'perfiles')

    perfiles = ma.Nested(UsuarioPerfilSchema, many=True)


class UsuarioAccesosGestionSchema(ma.Schema):
    class Meta:
        fields = ('idusuario','nombre','correoelectronico','activo')


class UsuarioInfoSchema(ma.Schema):
    class Meta:
        fields = ('idusuario','nombre','correoelectronico','activo','perfiles')
    
    perfiles = ma.Nested(UsuarioPerfilInfoSchema, many=True)
