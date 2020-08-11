from flask import request
from flask_restful import Resource
from dao.flask_config import app
from service.jobposition_candidate_service import JobPositionCandidateService
from service.selectionprocess_candidate_service import SelectionProcessCandidateService

jobposition_candidate_service = JobPositionCandidateService()
selectionprocess_candidate_service = SelectionProcessCandidateService()

class JobPositionCandidateController(Resource):
    
    def get(self, idclient=None, idjobposition=None, idcandidate=None):
        return jobposition_candidate_service.get_jobposition_candidates(idclient, idjobposition, idcandidate)

    def post(self):
        idclient = request.json['idclient']
        idjobposition = request.json['idjobposition']
        idcandidate = request.json['idcandidate']
        
        new_jobposition_candidate = jobposition_candidate_service.add_jobposition_candidate(idclient, idjobposition, idcandidate)
        
        date_registered = request.json['date_registered']
        user_register = request.json['user_register']
        user_registered_byself = request.json['user_registered_byself']
        
        new_selectionprocess = selectionprocess_candidate_service.add_selectionprocess(idclient, idjobposition, idcandidate, date_registered, user_register, user_registered_byself)
        
        return new_jobposition_candidate

    def delete(self):
        idclient = request.json['idclient']
        idjobposition = request.json['idjobposition']
        idcandidate = request.json['idcandidate']
        
        jobposition_candidate = jobposition_candidate_service.delete_jobposition_candidate(idclient, idjobposition, idcandidate)
        selectionprocess_candidate_service.delete_selectionprocess(idclient, idjobposition, idcandidate)

        return jobposition_candidate