from flask import jsonify
from dao.flask_config import db
from object.candidate import Candidate, CandidateInfoSimpleSchema

candidate_schema = CandidateInfoSimpleSchema()
candidates_schema = CandidateInfoSimpleSchema(many=True)

class CandidateInfoService():

    def get_candidates(self, idcandidate):        
        if idcandidate:
            all_selectionprocess = Candidate.query.filter(Candidate.idcandidato==idcandidate).all()
        else:
            all_selectionprocess = Candidate.query.all()
        
        if all_selectionprocess:
            result = candidates_schema.dump(all_selectionprocess)
            return jsonify(result)
        return {'message': 'Not found'}, 404
