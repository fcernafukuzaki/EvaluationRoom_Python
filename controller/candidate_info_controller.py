from flask_restful import Resource
from service.candidate_info_service import CandidateInfoService

candidate_info_service = CandidateInfoService()

class CandidateInfoSimpleController(Resource):
    
    def get(self, idcandidate=None):
        return candidate_info_service.get_candidates(idcandidate)
