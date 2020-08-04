from flask import jsonify
from common.util import str2bool
from dao.flask_config import db
from object.selectionprocess import SelectionProcess, SelectionProcessSchema

selectionprocess_schema = SelectionProcessSchema()
selectionprocesses_schema = SelectionProcessSchema(many=True)

class SelectionProcessService():

    def get_selectionprocesses(self, idclient, idjobposition):        
        if idclient and idjobposition:
            all_selectionprocess = SelectionProcess.query.filter(SelectionProcess.idclient==idclient, SelectionProcess.idjobposition==idjobposition).all()
        elif idclient and not idjobposition:
            all_selectionprocess = SelectionProcess.query.filter(SelectionProcess.idclient==idclient).all()
        elif not idclient and idjobposition:
            return {'message': 'Client identity is required'}, 500
        else:
            all_selectionprocess = SelectionProcess.query.all()
        
        if all_selectionprocess:
            result = selectionprocesses_schema.dump(all_selectionprocess)
            return jsonify(result)
        return {'message': 'Not found'}, 404

    def add_selectionprocess(self, idclient, idjobposition, date_process_begin, date_process_end, user_register, process_active):
        process_active = str2bool(process_active)

        new_selectionprocess = SelectionProcess(idclient, idjobposition, date_process_begin, date_process_end, user_register, process_active)
        db.session.add(new_selectionprocess)
        db.session.commit()
        return selectionprocess_schema.jsonify(new_selectionprocess)
    
    def update_selectionprocess(self, idclient, idjobposition, date_process_begin, date_process_end, user_register, process_active):
        process_active = str2bool(process_active)

        selectionprocess = SelectionProcess.query.get((idclient, idjobposition))
        selectionprocess.date_process_begin = date_process_begin
        selectionprocess.date_process_end = date_process_end
        selectionprocess.user_register = user_register
        selectionprocess.process_active = process_active

        db.session.commit()
        return selectionprocess_schema.jsonify(selectionprocess)

    def delete_selectionprocess(self, idclient, idjobposition):
        selectionprocess = SelectionProcess.query.get((idclient, idjobposition))

        db.session.delete(selectionprocess)
        db.session.commit()

        return selectionprocess_schema.jsonify(selectionprocess)