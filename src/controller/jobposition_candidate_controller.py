from flask import request
from flask_restful import Resource
from dao.flask_config import app
from service.jobposition_candidate_service import JobPositionCandidateService

jobposition_candidate_service = JobPositionCandidateService()

class JobPositionCandidateController(Resource):
    
    def get(self, idclient=None, idjobposition=None, idcandidate=None):
        return jobposition_candidate_service.get_jobposition_candidates(idclient, idjobposition, idcandidate)

    def post(self):
        idclient = request.json['idclient']
        idjobposition = request.json['idjobposition']
        idcandidate = request.json['idcandidate']
        
        new_jobposition_candidate = jobposition_candidate_service.add_jobposition_candidate(idclient, idjobposition, idcandidate)
        
        return new_jobposition_candidate

    def delete(self):
        idclient = request.json['idclient']
        idjobposition = request.json['idjobposition']
        idcandidate = request.json['idcandidate']
        
        return jobposition_candidate_service.delete_jobposition_candidate(idclient, idjobposition, idcandidate)