from flask import jsonify
from objects.candidate import Candidate
from objects.candidate_info import CandidateInfo, CandidateInfoSchema

candidates_info_schema = CandidateInfoSchema(many=True)

class CandidateInfoService():

    def get_candidates(self, idcandidate):        
        if idcandidate:
            all_candidates = Candidate.query.filter(Candidate.idcandidato==idcandidate).all()
        else:
            all_candidates = CandidateInfo.all_candidates_resumen
        
        if all_candidates:
            result = candidates_info_schema.dump(all_candidates)
            return jsonify(result)
        return {'message': 'Not found'}, 404
