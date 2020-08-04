from flask import request
from flask_restful import Resource
from dao.flask_config import app
from service.selectionprocess_service import SelectionProcessService

selectionprocess_service = SelectionProcessService()

class SelectionProcessController(Resource):
    
    def get(self, idclient=None, idjobposition=None):
        return selectionprocess_service.get_selectionprocesses(idclient, idjobposition)

    def post(self):
        idclient = request.json['idclient']
        idjobposition = request.json['idjobposition']
        date_process_begin = request.json['date_process_begin']
        date_process_end = request.json['date_process_end']
        user_register = request.json['user_register']
        process_active = request.json['process_active']
        
        new_selectionprocess = selectionprocess_service.add_selectionprocess(idclient, idjobposition, date_process_begin, date_process_end, user_register, process_active)
        
        return new_selectionprocess

    def put(self):
        idclient = request.json['idclient']
        idjobposition = request.json['idjobposition']
        date_process_begin = request.json['date_process_begin']
        date_process_end = request.json['date_process_end']
        user_register = request.json['user_register']
        process_active = request.json['process_active']

        return selectionprocess_service.update_selectionprocess(idclient, idjobposition, date_process_begin, date_process_end, user_register, process_active)

    def delete(self):
        idclient = request.json['idclient']
        idjobposition = request.json['idjobposition']

        return selectionprocess_service.delete_selectionprocess(idclient, idjobposition)