from flask import jsonify
from dao.flask_config import db
from dao.object.candidate import Candidate, CandidateSchema

candidate_schema = CandidateSchema()
candidates_schema = CandidateSchema(many=True)

class CandidateService():

    def get_candidates(self, idcandidate):        
        if idcandidate:
            all_selectionprocess = Candidate.query.filter(Candidate.idcandidato==idcandidate).all()
        else:
            all_selectionprocess = Candidate.query.all()
        
        if all_selectionprocess:
            result = candidates_schema.dump(all_selectionprocess)
            return jsonify(result)
        return {'message': 'Not found'}, 404

    def add_candidate(self, idcandidate, nombre, apellidopaterno):
        new_selectionprocess = Candidate(idcandidate, nombre, apellidopaterno)
        db.session.add(new_selectionprocess)
        db.session.commit()
        return candidate_schema.jsonify(new_selectionprocess)
    
    def update_candidate(self, idcandidate, nombre, apellidopaterno):
        selectionprocess = Candidate.query.get((idcandidate, nombre, apellidopaterno))
        selectionprocess.nombre = nombre
        selectionprocess.apellidopaterno = apellidopaterno

        db.session.commit()
        return candidate_schema.jsonify(selectionprocess)

    def delete_candidate(self, idcandidate, nombre, apellidopaterno):
        selectionprocess = Candidate.query.get((idclient, idjobposition, idcandidate))

        db.session.delete(selectionprocess)
        db.session.commit()

        return candidate_schema.jsonify(selectionprocess)