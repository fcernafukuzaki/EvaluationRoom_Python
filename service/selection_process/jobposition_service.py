from flask import jsonify
from configs.resources import db
from objects.selection_process.jobposition import JobPosition, JobPositionSchema

jobposition_schema = JobPositionSchema()
jobpositions_schema = JobPositionSchema(many=True)

class JobPositionService():

    def get_jobpositions(self, idclient):
        result, code, message = None, 404, 'No existen puestos laborales asignados.'
        if not idclient:
            code, message = 500, f'Identificador es requerido {e}'
        try:
            all_jobpositions = db.session.query(JobPosition).filter(JobPosition.idcliente==idclient).order_by(JobPosition.idcliente)

            if all_jobpositions.count():
                result, code, message = jobpositions_schema.dump(all_jobpositions), 200, 'Se encontró puestos laborales.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de puestos laborales en base de datos {e}'
        finally:
            print(message)
            return result, code, message
    
    def get_jobposition(self, idclient, idjobposition):
        result, code, message = None, 404, 'No existen puesto laboral.'
        if not idjobposition:
            code, message = 500, f'Identificador es requerido {e}'
        try:
            jobposition = db.session.query(JobPosition).filter(JobPosition.idcliente==idclient,JobPosition.idpuestolaboral==idjobposition).order_by(JobPosition.idcliente,JobPosition.idpuestolaboral).all()

            if jobposition:
                result, code, message = jobposition_schema.dump(jobposition[0]), 200, 'Se encontró puesto laboral.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de puesto laboral en base de datos {e}'
        finally:
            print(message)
            return result, code, message
        
    def add_jobposition(self, idclient, name):
        result = None
        try:
            new_jobposition = JobPosition(idclient, None, name)
            db.session.add(new_jobposition)
            db.session.commit()
            db.session.refresh(new_jobposition)
            result = (new_jobposition.idcliente, new_jobposition.idpuestolaboral)
            code, message = 200, 'Se registró puesto laboral en base de datos.'
        except Exception as e:
            code, message = 503, f'Hubo un error al registrar puesto laboral en base de datos {e}'
        finally:
            print(message)
            return result, code, message
    
    def update_jobposition(self, idclient, idjobposition, name):
        result = None
        try:
            jobposition = JobPosition.query.get((idclient, idjobposition))
            jobposition.nombre = name
            db.session.commit()
            result, code, message = idclient, 200, 'Se actualizó puesto laboral en base de datos.'
        except Exception as e:
            code, message = 503, f'Hubo un error al actualizar puesto laboral en base de datos {e}'
        finally:
            print(message)
            return result, code, message

    def delete_jobposition(self, idclient, idjobposition):
        result = None
        try:
            jobposition = JobPosition.query.get((idclient, idjobposition))
            db.session.delete(jobposition)
            db.session.commit()
            result, code, message = idclient, 200, 'Se eliminó puesto laboral en base de datos.'
        except Exception as e:
            code, message = 503, f'Hubo un error al eliminar puesto laboral en base de datos {e}'
        finally:
            print(message)
            return result, code, message