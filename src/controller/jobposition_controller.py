from flask import request
from flask_restful import Resource
from dao.flask_config import app
from service.jobposition_service import JobPositionService

jobposition_service = JobPositionService()

class JobPositionController(Resource):
    
    def get(self, idclient=None, idjobposition=None):
        return jobposition_service.get_jobpositions(idclient, idjobposition)

    def post(self):
        idclient = request.json['idclient']
        idjobposition = request.json['idjobposition']
        nombre = request.json['nombre']
        
        new_jobposition = jobposition_service.add_jobposition(idclient, idjobposition, nombre)
        
        return new_jobposition

    def put(self):
        idclient = request.json['idclient']
        idjobposition = request.json['idjobposition']
        nombre = request.json['nombre']

        return jobposition_service.update_jobposition(idclient, idjobposition, nombre)

    def delete(self):
        idclient = request.json['idclient']
        idjobposition = request.json['idjobposition']
        
        return jobposition_service.delete_jobposition(idclient, idjobposition)