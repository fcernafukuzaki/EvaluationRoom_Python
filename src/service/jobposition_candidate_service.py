from flask import jsonify
from dao.flask_config import db
from object.jobposition_candidate import JobPositionCandidate, JobPositionCandidateSchema

jobposition_candidate_schema = JobPositionCandidateSchema()
jobpositions_candidate_schema = JobPositionCandidateSchema(many=True)

class JobPositionCandidateService():

    def get_jobposition_candidates(self, idclient, idjobposition, idcandidate):
        if idclient and idjobposition:
            all_jobpositions = JobPositionCandidate.query.filter(JobPositionCandidate.idcliente==idclient, JobPositionCandidate.idpuestolaboral==idjobposition).order_by(JobPositionCandidate.idcandidato)
        elif idclient and not idjobposition:
            all_jobpositions = JobPositionCandidate.query.filter(JobPositionCandidate.idcliente==idclient).order_by(JobPositionCandidate.idcliente, JobPositionCandidate.idpuestolaboral, JobPositionCandidate.idcandidato)
        elif not idclient and idjobposition:
            return {'message': 'Client identity is required'}, 500
        else:
            all_jobpositions = JobPositionCandidate.query.all()
        
        if all_jobpositions and idclient and idjobposition:
            result = jobpositions_candidate_schema.jsonify(all_jobpositions)
            return result
        else:
            result = jobpositions_candidate_schema.dump(all_jobpositions)
            return jsonify(result)
        return {'message': 'Not found'}, 404
        
    def add_jobposition_candidate(self, idclient, idjobposition, idcandidate):
        print(idclient)
        print(idjobposition)
        print(idcandidate)
        new_jobposition = JobPositionCandidate(idclient, idjobposition, idcandidate)
        db.session.add(new_jobposition)
        db.session.commit()
        return jobposition_candidate_schema.jsonify(new_jobposition)
    
    def delete_jobposition_candidate(self, idclient, idjobposition, idcandidate):
        jobposition = JobPositionCandidate.query.get((idclient, idjobposition, idcandidate))

        db.session.delete(jobposition)
        db.session.commit()

        return jobposition_candidate_schema.jsonify(jobposition)