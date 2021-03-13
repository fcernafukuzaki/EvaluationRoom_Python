from flask import request
from flask_restful import Resource
from ..flask_config import app
from service.candidate_service import CandidateService

candidate_service = CandidateService()

class CandidateController(Resource):
    
    def get(self, idcandidate=None):
        return candidate_service.get_candidates(idcandidate)

    def post(self):
        idcandidate = request.json['idcandidate']
        nombre = request.json['nombre']
        apellidopaterno = request.json['apellidopaterno']
        
        new_selectionprocess = candidate_service.add_candidate(idcandidate, nombre, apellidopaterno)
        
        return new_selectionprocess

    def put(self):
        idcandidate = request.json['idcandidate']
        nombre = request.json['nombre']
        apellidopaterno = request.json['apellidopaterno']

        return candidate_service.update_candidate(idcandidate, nombre, apellidopaterno)

    def delete(self):
        idcandidate = request.json['idcandidate']
        nombre = request.json['nombre']
        apellidopaterno = request.json['apellidopaterno']

        return candidate_service.delete_candidate(idcandidate, nombre, apellidopaterno)