from configs.flask_config import db, ma


class SoporteTecnicoNotificacion(db.Model):
    __table_args__ = {"schema": "evaluationroom"}
    __tablename__ = 'soportetecnico_notificacion'

    correoelectronico = db.Column(db.String(), primary_key=True)
    fecharegistro = db.Column(db.DateTime(), primary_key=True)
    observacion = db.Column(db.String(), primary_key=True)
    detalle = db.Column(db.String())

    def __init__(self, correo_electronico, fecha_registro, observacion, detalle=None):
        self.correoelectronico = correo_electronico
        self.fecharegistro = fecha_registro
        self.observacion = observacion
        self.detalle = detalle

class SoporteTecnicoNotificacionSchema(ma.Schema):
    class Meta:
        fields = ('correoelectronico', 'fecharegistro', 'observacion', 'detalle')
