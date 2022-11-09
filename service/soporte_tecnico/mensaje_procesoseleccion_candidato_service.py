from configs.flask_config import db
from sqlalchemy import func
from objects.soporte_tecnico.mensaje_procesoseleccion_candidato import MensajeProcesoseleccionCandidato, MensajeProcesoseleccionCandidatoSchema

mensaje_procesoseleccion_candidato_schema = MensajeProcesoseleccionCandidatoSchema(many=True)

class MensajeProcesoseleccionCandidatoService():

    def _consultar_mensajes_error(self):
        return db.session.query(
                    MensajeProcesoseleccionCandidato
                ).filter(func.substr(MensajeProcesoseleccionCandidato.tipo_mensaje, 0, len('mensaje_error') + 1) == 'mensaje_error'
                ).order_by(MensajeProcesoseleccionCandidato.id_mensaje)

    def obtener_mensajes_error(self):
        try:
            mensajes_error = self._consultar_mensajes_error()
        except:
            print('Error al recuperar el mensaje de error.')
            return 'Error al recuperar el mensaje de error.'
        else:
            if mensajes_error.count() > 0:
                return {'mensajes': mensaje_procesoseleccion_candidato_schema.dump(mensajes_error)}, 200
            return None
