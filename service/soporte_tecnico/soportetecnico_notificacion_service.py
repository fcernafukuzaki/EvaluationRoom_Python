from configs.resources import db
from sqlalchemy import func
from objects.soporte_tecnico.soportetecnico_notificacion import SoporteTecnicoNotificacion
import json

class SoporteTecnicoNotificacionService():

    def guardar_mensaje_error_candidato(self, correo_electronico, observacion, detalle=None):
        try:
            nuevo_mensaje_error_candidato = SoporteTecnicoNotificacion(correo_electronico, func.now(), observacion, json.dumps(detalle))

            db.session.add(nuevo_mensaje_error_candidato)
            db.session.commit()

            return True, 'Registro exitoso.'
        except:
            print('Error al registrar notificación de error del candidato {}.'.format(correo_electronico))
            return False, 'Error al registrar notificación de error.'
