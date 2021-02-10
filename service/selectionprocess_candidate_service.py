from flask import jsonify
from sqlalchemy import desc
from common.util import str2bool
from dao.flask_config import db
from dao.object.selectionprocess_candidate import SelectionProcessCandidate, SelectionProcessCandidateSchema

selectionprocess_candidate_schema = SelectionProcessCandidateSchema()
selectionprocess_candidates_schema = SelectionProcessCandidateSchema(many=True)

class SelectionProcessCandidateService():

    def get_selectionprocesses(self, idclient, idjobposition):        
        if idclient and idjobposition:
            all_selectionprocess = SelectionProcessCandidate.query.filter(SelectionProcessCandidate.idclient==idclient, SelectionProcessCandidate.idjobposition==idjobposition).all()
        elif idclient and not idjobposition:
            all_selectionprocess = SelectionProcessCandidate.query.filter(SelectionProcessCandidate.idclient==idclient).all()
        elif not idclient and idjobposition:
            return {'message': 'Client identity is required'}, 500
        else:
            all_selectionprocess = SelectionProcessCandidate.query.order_by(desc(SelectionProcessCandidate.idjobposition)).all()
        
        if all_selectionprocess:
            result = selectionprocess_candidates_schema.dump(all_selectionprocess)
            return jsonify(result)
        return {'message': 'Not found'}, 404

    def add_selectionprocess(self, idclient, idjobposition, idcandidate, date_registered, user_register, user_registered_byself):
        user_registered_byself = str2bool(user_registered_byself)

        new_selectionprocess = SelectionProcessCandidate(idclient, idjobposition, idcandidate, date_registered, user_register, user_registered_byself)
        db.session.add(new_selectionprocess)
        db.session.commit()
        return selectionprocess_candidate_schema.jsonify(new_selectionprocess)
    
    def update_selectionprocess(self, idclient, idjobposition, idcandidate, date_registered, user_register, user_registered_byself):
        user_registered_byself = str2bool(user_registered_byself)

        selectionprocess = SelectionProcessCandidate.query.get((idclient, idjobposition, idcandidate))
        selectionprocess.date_registered = date_registered
        selectionprocess.user_register = user_register
        selectionprocess.user_registered_byself = user_registered_byself

        db.session.commit()
        return selectionprocess_candidate_schema.jsonify(selectionprocess)

    def delete_selectionprocess(self, idclient, idjobposition, idcandidate):
        selectionprocess = SelectionProcessCandidate.query.get((idclient, idjobposition, idcandidate))

        db.session.delete(selectionprocess)
        db.session.commit()

        return selectionprocess_candidate_schema.jsonify(selectionprocess)