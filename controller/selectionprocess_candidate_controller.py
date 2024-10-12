from flask import request
from flask_restful import Resource
from configs.resources import app
from service.selectionprocess_candidate_service import SelectionProcessCandidateService

selectionprocess_candidate_service = SelectionProcessCandidateService()

class SelectionProcessCandidateController(Resource):
    
    def get(self, idclient=None, idjobposition=None):
        return selectionprocess_candidate_service.get_selectionprocesses(idclient, idjobposition)

    def post(self):
        idclient = request.json['idclient']
        idjobposition = request.json['idjobposition']
        idcandidate = request.json['idcandidate']
        date_registered = request.json['date_registered']
        user_register = request.json['user_register']
        user_registered_byself = request.json['user_registered_byself']
        
        new_selectionprocess = selectionprocess_candidate_service.add_selectionprocess(idclient, idjobposition, idcandidate, date_registered, user_register, user_registered_byself)
        
        return new_selectionprocess

    def put(self):
        idclient = request.json['idclient']
        idjobposition = request.json['idjobposition']
        idcandidate = request.json['idcandidate']
        date_registered = request.json['date_registered']
        user_register = request.json['user_register']
        user_registered_byself = request.json['user_registered_byself']

        return selectionprocess_candidate_service.update_selectionprocess(idclient, idjobposition, idcandidate, date_registered, user_register, user_registered_byself)

    def delete(self):
        idclient = request.json['idclient']
        idjobposition = request.json['idjobposition']
        idcandidate = request.json['idcandidate']

        return selectionprocess_candidate_service.delete_selectionprocess(idclient, idjobposition, idcandidate)