from flask import request
from flask_restful import Resource
from configs.flask_config import app
from service.jobposition_service import JobPositionService
from service.selectionprocess_service import SelectionProcessService

jobposition_service = JobPositionService()
selectionprocess_service = SelectionProcessService()

class JobPositionController(Resource):
    
    def get(self, idclient=None, idjobposition=None):
        return jobposition_service.get_jobpositions(idclient, idjobposition)

    def post(self):
        idclient = request.json['idclient']
        nombre = request.json['nombre']
        
        new_jobposition_json, new_jobposition = jobposition_service.add_jobposition(idclient, None, nombre)
        
        date_process_begin = request.json['date_process_begin']
        date_process_end = request.json['date_process_end']
        user_register = request.json['user_register']
        process_active = request.json['process_active']
        
        new_selectionprocess = selectionprocess_service.add_selectionprocess(idclient, new_jobposition.idpuestolaboral, date_process_begin, date_process_end, user_register, process_active)
        
        return new_jobposition_json

    def put(self):
        idclient = request.json['idclient']
        idjobposition = request.json['idjobposition']
        nombre = request.json['nombre']

        jobposition = jobposition_service.update_jobposition(idclient, idjobposition, nombre)

        date_process_begin = request.json['date_process_begin']
        date_process_end = request.json['date_process_end']
        user_register = request.json['user_register']
        process_active = request.json['process_active']

        selectionprocess = selectionprocess_service.update_selectionprocess(idclient, idjobposition, date_process_begin, date_process_end, user_register, process_active)

        return jobposition

    def delete(self):
        idclient = request.json['idclient']
        idjobposition = request.json['idjobposition']
        
        return jobposition_service.delete_jobposition(idclient, idjobposition)