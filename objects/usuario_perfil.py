from configs.resources import db, ma
from objects.perfil import Perfil, PerfilSchema


class UsuarioPerfil(db.Model):
    __table_args__ = {"schema": "evaluationroom", 'extend_existing': True}
    __tablename__ = 'usuarioperfil'

    idusuario = db.Column(db.Integer, db.ForeignKey('evaluationroom.usuario.idusuario'), primary_key=True)
    idperfil = db.Column(db.Integer, db.ForeignKey('evaluationroom.perfil.idperfil'), primary_key=True)
    
    perfil = db.relationship('Perfil', 
                             primaryjoin='and_(UsuarioPerfil.idperfil==Perfil.idperfil)',
                             order_by="Perfil.idperfil")
    
    def __init__(self, idusuario, idperfil):
        self.idusuario = idusuario
        self.idperfil = idperfil


class UsuarioPerfilSchema(ma.Schema):
    class Meta:
        fields = ('idperfil', 'idusuario')


class UsuarioPerfilInfoSchema(ma.Schema):
    class Meta:
        fields = ('idperfil', 'idusuario', 'perfil')
    
    perfil = ma.Nested(PerfilSchema)
