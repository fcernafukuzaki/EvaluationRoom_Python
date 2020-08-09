from flask import jsonify
from dao.flask_config import db
from object.jobposition import JobPosition, JobPositionSchema

jobposition_schema = JobPositionSchema()
jobpositions_schema = JobPositionSchema(many=True)

class JobPositionService():

    def get_jobpositions(self, idclient, idjobposition):
        if idclient and idjobposition:
            all_jobpositions = JobPosition.query.get((idclient, idjobposition))
        elif idclient and not idjobposition:
            all_jobpositions = JobPosition.query.filter(JobPosition.idcliente==idclient).order_by(JobPosition.idpuestolaboral)
        elif not idclient and idjobposition:
            return {'message': 'Client identity is required'}, 500
        else:
            all_jobpositions = JobPosition.query.all()
        
        if all_jobpositions and idclient and idjobposition:
            result = jobposition_schema.jsonify(all_jobpositions)
            return result
        else:
            result = jobpositions_schema.dump(all_jobpositions)
            return jsonify(result)
        return {'message': 'Not found'}, 404
        
    def add_jobposition(self, idclient, idjobposition, name):
        new_jobposition = JobPosition(idclient, idjobposition, name)
        db.session.add(new_jobposition)
        db.session.commit()
        return jobposition_schema.jsonify(new_jobposition)
    
    def update_jobposition(self, idclient, idjobposition, name):
        jobposition = JobPosition.query.get((idclient, idjobposition))
        jobposition.nombre = name
        
        db.session.commit()
        return jobposition_schema.jsonify(jobposition)

    def delete_jobposition(self, idclient, idjobposition):
        jobposition = JobPosition.query.get((idclient, idjobposition))

        db.session.delete(jobposition)
        db.session.commit()

        return jobposition_schema.jsonify(jobposition)